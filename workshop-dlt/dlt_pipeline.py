"""Pull one Pydantic Logfire trace into DuckDB via dlt.

Based on dltHub's Logfire context (https://dlthub.com/context/source/logfire).
The Query API is a single SQL-over-HTTP call, not a paginated listing, so this
is a plain @dlt.resource generator instead of dlt.sources.rest_api — one HTTP
call, response transposed into row dicts, dlt normalizes the nested
`attributes` JSON into child tables from there.
"""

import os
import time

import dlt
import requests

LOGFIRE_QUERY_URL = "https://logfire-us.pydantic.dev/v1/query"


def _columns_to_rows(payload: dict) -> list[dict]:
    """Transpose Logfire's {"columns": [{"name", "values": [...]}]} into row dicts."""
    columns = payload["columns"]
    if not columns:
        return []
    n_rows = len(columns[0]["values"])
    return [
        {col["name"]: col["values"][i] for col in columns}
        for i in range(n_rows)
    ]


def _query_with_retry(sql: str, read_token: str, max_attempts: int = 5) -> dict:
    """The free-tier Query API rate-limits (429) under repeated calls; back off and retry."""
    for attempt in range(max_attempts):
        response = requests.get(
            LOGFIRE_QUERY_URL,
            headers={"Authorization": f"Bearer {read_token}"},
            params={"sql": sql},
            timeout=30,
        )
        if response.status_code == 429 and attempt < max_attempts - 1:
            time.sleep(2**attempt * 5)
            continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError("unreachable")


def wait_for_trace(trace_id: str, expected_span_count: int, read_token: str, max_wait_seconds: int = 60) -> int:
    """Poll until every span of a freshly-created trace is queryable (ingestion lag)."""
    sql = f"SELECT COUNT(*) AS n FROM records WHERE trace_id = '{trace_id}'"
    waited = 0
    while waited < max_wait_seconds:
        payload = _query_with_retry(sql, read_token)
        n = payload["columns"][0]["values"][0]
        if n >= expected_span_count:
            return n
        time.sleep(5)
        waited += 5
    return n


@dlt.resource(name="traces", write_disposition="replace")
def logfire_traces(trace_id: str, read_token: str = dlt.secrets.value):
    """Pull every span belonging to one trace from the Logfire Query API."""
    sql = f"""
        SELECT
            trace_id, span_id, parent_span_id, span_name, kind,
            start_timestamp, end_timestamp, duration,
            level, is_exception, attributes
        FROM records
        WHERE trace_id = '{trace_id}'
        ORDER BY start_timestamp
    """
    payload = _query_with_retry(sql, read_token)
    yield _columns_to_rows(payload)


def run(trace_id: str):
    # pipeline_name must differ from dataset_name, or DuckDB raises
    # "Ambiguous reference to catalog or schema" (same catalog/schema name
    # collision noted in the workshop's own rest_api_pipeline.py example).
    # dataset_name stays "agent_traces" to match the homework's SQL check.
    pipeline = dlt.pipeline(
        pipeline_name="logfire_ingest",
        destination="duckdb",
        dataset_name="agent_traces",
    )
    read_token = os.environ["LOGFIRE_READ_TOKEN"]
    load_info = pipeline.run(logfire_traces(trace_id=trace_id, read_token=read_token))
    return pipeline, load_info


if __name__ == "__main__":
    import sys

    from dotenv import load_dotenv

    load_dotenv()
    trace = sys.argv[1]
    pipeline, info = run(trace)
    print(info)
