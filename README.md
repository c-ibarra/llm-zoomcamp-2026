# LLM Zoomcamp 2026

Personal solutions and project for the [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp/) cohort by DataTalksClub.

## Structure

- `hw1-agentic-rag/` — Homework 1: Agentic RAG
- `hw2-vector-search/` — Homework 2: Vector Search
- `hw3-orchestration/` — Homework 3: Orchestration with Kestra
- `hw4-evaluation/` — Homework 4: Evaluation
- `hw5-monitoring/` — Homework 5: Monitoring
- `capstone/` — Capstone project

## Secrets

This project requires an OpenAI API key.

**Option 1 — 1Password (recommended):** store the key in a vault item and run `direnv allow` — the `.envrc` loads it automatically on `cd`.

**Option 2 — `.env` file:** create a `.env` file in the project root (already in `.gitignore`) with:

```
OPENAI_API_KEY=sk-...
```

The notebooks load the key automatically: first from 1Password, then from `.env`.

## Student

GitHub: [c-ibarra](https://github.com/c-ibarra)

