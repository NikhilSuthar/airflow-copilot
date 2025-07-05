# 🤖 Agent Workflow

**Airflow Copilot** uses a **LangGraph-based, tool‑driven agent** to transform plain‑language conversations into secure and auditable Airflow API calls.

---

![Agent Workflow Diagram](../assets/Airflow-Workflow.svg){ .center-img }

*🧭 Each user message flows through summarization (if needed), model reasoning, and tool execution via LangGraph.*

---

## 🔁 Workflow Overview

Every user message flows through the following loop:

| Step | Node                | Purpose                                                                                  |
|------|---------------------|------------------------------------------------------------------------------------------|
| 1️⃣   | **Summarize**       | Condenses earlier messages into a short summary to keep context lightweight *(see Summarization)* |
| 2️⃣   | **Model Call**      | The LLM decides whether to respond directly or invoke one or more tools                 |
| 3️⃣   | **Tool Node**       | Executes one or more Airflow tools asynchronously and returns results                   |
| 🔄   | **Conditional Edge** | If tool calls remain, loops back to Tool Node; otherwise, finalizes the user response   |
| ✅   | **END**              | Delivers the natural‑language reply or tool output to the user                          |

---

## 📦 State Management

LangGraph maintains conversation history across sessions and redeployments using persistent checkpoints stored in PostgreSQL.

- **Thread ID** — Each user conversation is tracked using their Microsoft Teams ID.
- **Summarization** — Older messages are trimmed into concise summaries (3–4 lines) to reduce input length. Note: messages are logically removed from state, but still stored in the backend.
- **PostgreSQL Checkpointer** — Persists state transitions after every model/tool interaction, enabling recovery from crashes and safe concurrency.

---

## 🛠️ Tool Execution Flow

1. The LLM generates tool calls like `get_all_dags`, `trigger_dag`, etc.
2. The **Tool Node** handles each tool call:
   - Extracts and builds the full API request (`url`, `method`, `payload`)
   - Resolves credentials (centralized or per-user)
   - Makes the HTTP request via **httpx** (asynchronously with retries)
   - Returns the response content
3. If no additional tool calls remain, the agent composes and sends the final natural‑language message.


---

## 🌍 Supported LLM Providers

Airflow Copilot is **LLM-agnostic** — just configure the appropriate environment variables, and the agent loads the correct SDK at runtime:

| Provider        | Env Prefix         | Example Model      |
|----------------|--------------------|--------------------|
| **OpenAI**      | `OPENAI_`           | `gpt-4o`           |
| **Google GenAI**| `GOOGLE_GENAI_`     | `gemini-pro`       |
| **Anthropic**   | `ANTHROPIC_`        | `claude-3-opus`    |

> You can use one provider for core reasoning, and another for summarization or low-cost background tasks.

---

## ⚡ Key Advantages

- **Concurrency‑Friendly**: Async architecture and Postgres checkpointer support many Teams users at once.
- **Lightweight Context**: Smart summarization keeps LLM input compact and relevant.
- **Tool Security**: The LLM is limited to a predefined set of tools—it cannot invent or manipulate endpoints.

---

## 🔗 Next Steps

- **[Message Summarization](/architecture/summarization)**: Understand the Agent workflow.
- **[Supported Airflow Copilot Features](/architecture/supported_apis)**: List of activity Airflow copilot can do.
- **[Environment Variables](/configuration/environment_variables)**: Configration details of Airflow Copilot.
