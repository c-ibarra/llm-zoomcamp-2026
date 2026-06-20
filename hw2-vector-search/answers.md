# HW2 — Vector Search: Answers

LLM Zoomcamp 2026 · Deadline: 29 June 2026

Submit at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw2

---

| Q | Question | Answer |
|---|---|---|
| Q1 | First value `v[0]` of the ANN query embedding | `-0.02` |
| Q2 | Cosine similarity with `07-sqlitesearch-vector.md` | `0.37` |
| Q3 | File containing the highest-scoring chunk (ANN query) | `02-vector-search/lessons/07-sqlitesearch-vector.md` |
| Q4 | First result from minsearch VectorSearch (evaluation query) | `04-evaluation/lessons/05-search-metrics.md` |
| Q5 | File in vector results but NOT in keyword results (PostgreSQL query) | `02-vector-search/lessons/08-pgvector.md` |
| Q6 | First result after RRF hybrid search (tools query) | `01-agentic-rag/lessons/13-function-calling.md` |

---

## Setup used

- Model: `Xenova/all-MiniLM-L6-v2` (ONNX Runtime, 384 dimensions)
- Data: 72 lesson pages from commit `8c1834d`
- Chunking: `size=2000`, `step=1000` → 295 chunks
- Hybrid search: RRF with `k=60`

See [`solution.ipynb`](solution.ipynb) for full code and outputs.
