<div align="center">

# Airflow Copilot  
**Chat‑driven orchestration for Apache Airflow inside Microsoft Teams**

[![Docker](https://img.shields.io/docker/pulls/thedatacarpenter/airflow-copilot)](https://hub.docker.com/r/thedatacarpenter/airflow-copilot)
[![License](https://img.shields.io/github/license/NikhilSuthar/airflow-copilot)](LICENSE)

</div>

<div align="center">
<img src="docs/assets/AirflowCopilotLogo.svg" height="110" alt="Airflow Copilot logo">
</div>

## ✨ Why Copilot?

- **Conversational control** — trigger DAGs, view runs, pause/resume schedules, inspect logs.
- **LLM‑powered intelligence** — plug in OpenAI · Gemini · Claude · Groq.
- **RBAC aware** — honours Airflow permissions when calling its REST API.
- **Persistent memory** — summaries & checkpoints stored in PostgreSQL (LangGraph).
- **Deployment parity** — same image on Docker Compose, Kubernetes, ECS.

---

## 🚀 Quick Start (local)

> Full guide → **[`docs/quickstart/getting_started.md`](docs/quickstart/getting_started.md)**

```bash
# Clone & copy env template
git clone https://github.com/NikhilSuthar/airflow-copilot.git
cd airflow-copilot
cp .env.example .env            # fill in keys / secrets

# Launch Copilot + ngrok + bot‑updater
docker compose -f docker-compose.local.yml up -d
```

1. Ensure Airflow (≥ 2.5) is reachable at `${AIRFLOW_BASE_URL}`  
2. Ngrok publishes an HTTPS tunnel  
3. *bot‑updater* patches the Azure Bot endpoint automatically  
4. Open **Microsoft Teams** → chat with **Airflow Copilot** 🚀

---

## 🧠 Architecture

![Architecture](docs/assets/quick-start-arch.svg)

Read the deep dive → **[`docs/architecture/architecture.md`](docs/architecture/architecture.md)**

---

## 📦 Deployment Options

| Mode | Guide | Best For |
|------|-------|----------|
| Docker Compose (local) | [`docs/quickstart/getting_started.md`](docs/quickstart/getting_started.md) | Dev / PoC |
| Docker Compose (prod)  | [`docs/deployment/deployment.md`](docs/deployment/deployment.md#docker) | Small teams |
| Kubernetes             | [`docs/deployment/deployment.md`](docs/deployment/deployment.md#kubernetes) | Cloud & scale |

Each mode uses the **same `.env`**. Bring your own DB & TLS.

---

## ⚙️ Configuration

All runtime settings are environment variables.  
See the reference → **[`docs/configuration/environment_variables.md`](docs/configuration/environment_variables.md)**


---

## 📄 License

Licensed under the **MIT** License © 2025 Nikhil Suthar.

---

_🚀 Automate smarter. Collaborate better. — **Copilot**_