# LLM Zoomcamp 2026

End-to-end LLM engineering course by [DataTalksClub](https://github.com/DataTalksClub/llm-zoomcamp/), covering the full stack for building production-ready RAG systems and AI agents — from retrieval and embeddings to orchestration, evaluation, and monitoring.

## Modules

| # | Topic | Key concepts | Status |
|---|---|---|---|
| 1 | **Agentic RAG** | RAG pipeline, minsearch, chunking, agentic loop with function calling | ✅ Done |
| 2 | **Agents** | OpenAI Responses API, tool use, LangGraph, CrewAI | — |
| 3 | **Orchestration** | Kestra workflows, scheduling, pipeline coordination | — |
| 4 | **Evaluation** | Hit Rate, MRR, LLM-as-a-Judge, trajectory evaluation for agents | — |
| 5 | **Monitoring** | Streamlit, PostgreSQL, Grafana dashboards, Docker Compose | — |
| — | **Capstone** | Full RAG/agent system with ingestion, eval, UI, and monitoring | — |

## Tech Stack

- **LLM:** OpenAI API (GPT-4o-mini)
- **Search:** minsearch, ElasticSearch, pgvector
- **Agents:** toyaikit, LangGraph, CrewAI
- **Orchestration:** Kestra
- **Ingestion:** gitsource, dlt
- **Monitoring:** Streamlit, PostgreSQL, Grafana
- **Infrastructure:** Docker Compose, uv

## Homeworks

| HW | Topic | Notebook |
|---|---|---|
| HW1 | Agentic RAG | [hw1-agentic-rag/solution.ipynb](hw1-agentic-rag/solution.ipynb) |

## Setup

```bash
git clone https://github.com/c-ibarra/llm-zoomcamp-2026
cd llm-zoomcamp-2026
uv sync
```

### API Key

**Option 1 — 1Password:** store the key in a vault item and run `direnv allow`. The `.envrc` loads it automatically on `cd`.

**Option 2 — `.env` file:** create a `.env` file in the project root (already in `.gitignore`):

```
OPENAI_API_KEY=sk-...
```

The notebooks detect and load the key automatically from either source.

## Student

GitHub: [c-ibarra](https://github.com/c-ibarra)
