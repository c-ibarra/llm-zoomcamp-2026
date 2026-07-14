# HW4 — Evaluation: Answers

LLM Zoomcamp 2026

Submit at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4

---

| Q | Question | Answer |
|---|---|---|
| Q1 | Average input tokens across 3 structured-output calls (ground truth generation) | `1400` (observed avg 1353) |
| Q2 | `text_search` top-1 filename for `ground_truth[0]` | `01-agentic-rag/lessons/03-rag.md` |
| Q3 | `vector_search` top-1 filename for `ground_truth[0]` | `01-agentic-rag/lessons/01-intro.md` |
| Q4 | Hit Rate of `text_search` over the full ground truth | `0.76` (observed 0.758) |
| Q5 | MRR of `vector_search` over the full ground truth | `0.55` (observed 0.549) |
| Q6 | Best RRF `k` for `hybrid_search` | `1` (mrr=0.648, vs 0.638 tied for k=50/100/200) |

---

## Setup used

- Data: 72 lesson pages from commit `8c1834d`, chunked identically to HW2 (`size=2000, step=1000` → 295 chunks)
- Search: keyword (`minsearch.Index`), vector (`minsearch.VectorSearch` + ONNX `Xenova/all-MiniLM-L6-v2`), hybrid (RRF), reused from HW2
- Ground truth: 3 pages generated live for Q1 (`gpt-5.4-mini`, structured output); full 360-question dataset downloaded from the course repo for Q2–Q6
- Relevance matching: by `filename` (adapted from the course's `id`-based matching, since our knowledge base is lesson pages, not FAQ records)

See [`solution.ipynb`](solution.ipynb) for full code and outputs.
