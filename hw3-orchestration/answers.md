# HW3 — AI Orchestration with Kestra: Answers

LLM Zoomcamp 2026

Submit at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw3

---

| Q | Question | Answer |
|---|---|---|
| Q1 | Why does AI Copilot generate better Kestra flows than ChatGPT? | AI Copilot has access to current Kestra plugin documentation |
| Q2 | The non-RAG response about Kestra 1.1 features is best described as | Vague, generic, or fabricated — the model guesses from training data |
| Q3 | Output token count for `multilingual_agent` (`summary_length=short`) | 60-100 tokens (closest to observed 121) |
| Q4 | Output token ratio, long vs short summary | 2-5x more (observed ~1.8x) |
| Q5 | Output token ratio, 3-sentence vs 1-sentence `english_brevity` prompt | 2-4x more (observed ~1.7x) |
| Q6 | Best approach for deterministic, auditable production workflows | Use traditional task-based workflows for predictability and auditability |

---

## Evidence

### Q1 — ChatGPT vs Kestra AI Copilot

Prompt used: "Create a Kestra flow that loads NYC taxi data from a CSV file to BigQuery. The
flow should extract data, upload to GCS, and load to BigQuery."

Both tools were asked to configure `io.kestra.plugin.gcp.gcs.Upload` and
`io.kestra.plugin.gcp.bigquery.LoadFromGcs`. Checked against the official plugin docs:

- **ChatGPT** invented `bucket:` + `name:` on the Upload task and `projectId:` + `dataset:`
  + `table:` on LoadFromGcs — none of these properties exist on those tasks. The generated
  YAML would fail with an unknown-property error.
- **Kestra AI Copilot** used `to: "gs://bucket/path"` on Upload and
  `destinationTable: "project.dataset.table"` on LoadFromGcs — both are the real, current
  property names for these tasks.

This is direct evidence that Copilot is grounded in current, correct plugin documentation,
while a generic assistant hallucinates plausible-looking but non-existent syntax.

### Q2 — RAG vs No-RAG (Kestra 1.1 features)

- `1_chat_without_rag`: listed features like "Declarative Outputs", "Task Grouping", and new
  generic task types — plausible-sounding but not part of the actual Kestra 1.1 release. The
  flow's own log explicitly frames the response as likely outdated/generic.
- `2_chat_with_rag`: after ingesting the real Kestra 1.1 release notes, listed accurate,
  specific features — No-Code Dashboard Editor, Multi-Agent AI Systems, Fix with AI, Human
  Task (EE), and a list of specific new plugins.

### Q3 / Q4 — Token usage across summary lengths

`4_simple_agent`, `multilingual_agent` output token count (`log_token_usage`):

| Run | `summary_length` | Output tokens (`multilingual_agent`) |
|---|---|---|
| 1 | short | 121 |
| 2 | long | 215 |

Ratio: 215 / 121 ≈ 1.8x — well above the 20% "about the same" threshold, closer to the
2-5x bucket than to 10x+.

### Q5 — Prompt edit impact (`english_brevity`)

Edited the `english_brevity` task in `4_simple_agent.yaml`, changing the requested summary
length from "exactly 1 sentence" to "exactly 3 sentences". Both runs used
`summary_length=long`.

| Run | `english_brevity` prompt | Output tokens (`english_brevity`) |
|---|---|---|
| 1 (baseline) | exactly 1 sentence | 55 |
| 2 (edited)   | exactly 3 sentences | 95 |

Ratio: 95 / 55 ≈ 1.7x. Requesting 3x the sentence count did not produce a 3x token increase
— LLM output length doesn't scale linearly with a requested sentence count.

### Q6 — Best practices

Across Q2-Q5, the same question and the same flow configuration produced different token
counts and different response content run to run — LLM-backed steps are not deterministic
and their exact output can't be guaranteed or audited byte-for-byte. For workflows with
strict compliance requirements (financial reporting, regulated industries), predictable,
auditable task-based orchestration is the appropriate choice; AI agents are better suited to
exploratory or flexible tasks where some output variance is acceptable.

---

## Setup used

- Kestra `v1.3.21` (Docker Compose, local), Postgres backend
- Flows imported into the `zoomcamp` namespace via the REST API
  (`hw3-orchestration/flows/`)
- Secrets (`GEMINI_API_KEY`, `TAVILY_API_KEY`) resolved from 1Password at startup via
  `hw3-orchestration/scripts/start-kestra.sh` — never written to disk or committed
- Model: `gemini-2.5-flash` (chat/agents), `gemini-embedding-001` (RAG embeddings)
- All flow executions (Q2-Q5) run manually in the Kestra UI, logs read directly from each
  execution
