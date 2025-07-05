# Airflow Copilot 🛸

Chat‑first assistant for **Apache Airflow**. Run, monitor, and debug DAGs straight from Microsoft Teams using natural language.

[![Docker](https://img.shields.io/badge/Run%20with-Docker-blue)](deployment/docker-deployment.md)
[![License](https://img.shields.io/github/license/your-org/airflow-copilot)](license.md)

---

## Why Copilot?

| Pain | Copilot solution |
|------|------------------|
| Endless UI clicks to trigger or re‑run tasks | `@copilot trigger sales_daily` |
| Digging through logs for a failing task | `@copilot show last‑error for load_sales_data` |
| On‑call at 3 AM | Ask in Teams—no VPN, no browser tabs |

---

## Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/your-org/airflow-copilot.git
cd airflow-copilot

# 2. Spin up Airflow (optional if you already have one)
#    See https://airflow.apache.org/docs/...

# 3. Launch Copilot stack
docker compose -f docker-copilot-compose.yml up -d
```

Then open Teams, upload the `manifest.zip`, and say:

```
Hi Copilot, list dags
```

More details → **[Quick Start guide](docs/quickstart/getting_started.md)**

---

## Architecture in 30 sec

```
Teams  ──▶ Azure Bot Service ──▶ Copilot (FastAPI + LangGraph + LLM)
                           ▲
                           └── Airflow REST / PostgreSQL
```

- **LangGraph** stores memory & summaries in PostgreSQL  
- **Azure Bot** handles OAuth & message delivery  
- **Ngrok** (dev) or reverse proxy (prod) exposes Copilot

Full write‑up → [Architecture docs](docs/architecture/architecture.md)

---

## Configuration

| Env Var | Purpose |
|---------|---------|
| `LLM_MODEL_PROVIDER_NAME` | `OpenAI`, `Google_GenAI`, `Groq`, `Anthropic` |
| `AIRFLOW_BASE_URL` | Your Airflow REST endpoint |
| `FERNET_SECRET_KEY` | 32‑byte key for user tokens |

Complete list → [Environment variables](docs/configuration/environment_variables.md)

---

## Contributing

PRs & issues welcome!  
See [CONTRIBUTING](docs/contributing.md) for setup, style guide, and roadmap.

---

## License

Apache 2.0 — see [LICENSE](docs/license.md).
