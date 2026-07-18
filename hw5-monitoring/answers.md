# HW5 — Monitoring: Answers

LLM Zoomcamp 2026

Submit at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw5

---

| Q | Question | Answer |
|---|---|---|
| Q1 | Spans produced by one `rag()` call | `3` (`rag`, `search`, `llm`) |
| Q2 | Input tokens on the `llm` span | `7000` (observed 7111) |
| Q3 | Typical `llm` span duration | `Over 2000ms` (observed ~2.9s and ~3.4s across runs) |
| Q4 | Span names in the SQLite `spans` table | `rag`, `search`, and `llm` |
| Q5 | Span with the most total duration (excluding `rag`) | `llm` (~4.1s vs ~0.002s for `search`) |
| Q6 | Input token variation across 4 identical-query runs | `They're identical` (7111 all four times) |

---

## Setup used

- Data: same 72 lesson pages from commit `8c1834d`, `minsearch.Index` text search (no chunking) — the HW1 knowledge base, via the course's official starter (`starter.py`, `rag_helper.py`)
- Model: `gpt-5.4-mini` via the OpenAI Responses API
- Tracing: `opentelemetry-api` + `opentelemetry-sdk`, a `RAGTraced` subclass wrapping `rag()`/`search()`/`llm()` in spans
- Cost: same per-token rate as HW4 (`$0.75`/1M input, `$4.50`/1M output for `gpt-5.4-mini`)
- Persistence: custom `SQLiteSpanExporter` writing to `traces.db` (not committed — generated at notebook runtime)

See [`solution.ipynb`](solution.ipynb) for full code and outputs.
