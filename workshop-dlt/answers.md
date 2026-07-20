# dlt Workshop: Answers

LLM Zoomcamp 2026

Submit at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/dlt

---

| Q | Question | Answer |
|---|---|---|
| Q1 | Spans produced by one isolated agent run | `5` (observed 4-6: `invoke_agent`, 1-2x `chat`, 1-2x `execute_tool search`) |
| Q2 | Tables dlt created in the `agent_traces` schema | `24` (observed 22-24, varies with search-round count) |
| Q3 | Input token usage for the Q1 run | `1500-5000` (observed 1488-4109 across runs) |

---

## Setup used

- Agent: course's official Pydantic AI FAQ agent (`agent.py`, `ingest.py`, `main.py`), copied unmodified from `llm-zoomcamp/cohorts/2026/workshops/dlt/homework/`. Same FAQ dataset as Module 1, minsearch text search, now a `pydantic_ai.Agent` with a `search` tool
- Model: `gpt-5.4-mini`, via Pydantic AI's OpenAI integration
- Tracing: `logfire.configure()` + `logfire.instrument_pydantic_ai()`, plus a local `InMemorySpanExporter` to count spans for one isolated run without waiting on the Logfire API
- Ingestion: `dlt_pipeline.py`, a `@dlt.resource` generator hitting the Logfire Query API directly (bearer token, one SQL query per pull) rather than the generic `rest_api` builder, since it's not a paginated endpoint. Based on dltHub's Logfire context: https://dlthub.com/context/source/logfire
- Destination: local DuckDB, dataset `agent_traces` (had to keep this different from the dlt pipeline name or DuckDB throws an ambiguous schema error)
- Not committed: `logfire_ingest.duckdb`, generated fresh each run

See [`solution.ipynb`](solution.ipynb) for the full run, and [`dlt_pipeline.py`](dlt_pipeline.py) for the pipeline code.
