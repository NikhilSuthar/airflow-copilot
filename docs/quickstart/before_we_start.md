
# 🚦 Prerequisites

Before you spin‑up **Airflow Copilot**, make sure the following building blocks are in place.

- ✅ Install [Docker Community Edition (CE)](https://docs.docker.com/engine/install/) on your workstation (based on your OS).
- ✅ Install [Docker Compose](https://docs.docker.com/compose/install/) **v2.14.0 or newer**.

---

| # | Requirement | Why it’s needed | Minimum Version / Notes |
|---|-------------|-----------------|-------------------------|
| **1** | **Apache Airflow** | Target orchestrator Copilot queries (DAG runs, tasks, variables, etc.). | **≥ 2.5.0** <br>• REST API enabled |
| **2** | **Azure Bot Service** | Secure webhook & credentials so Microsoft Teams can talk to Copilot. | Any Azure subscription <br>• Consumes Bot Service units |
| **3** | **Microsoft Teams** | End‑user chat interface. Copilot is sideloaded as a custom Teams app. | Desktop / Web <br>• **Not** free “Community” edition |
| **4** | **PostgreSQL** | Persists conversation state & checkpoints (LangGraph). | v12 + <br>• Reuse Airflow DB **or** deploy fresh instance |

---

## 📝 More Context

### 1. Apache Airflow  
- Copilot calls the native REST API (`/api/v1/...`).
- Airflow must be reachable from the Copilot container (or vice‑versa).
- Use a dedicated service account (`admin` or fine‑grained RBAC).

### 2. Azure Bot Service  
- Acts as a relay: Teams ⇄ Bot Service ⇄ Copilot.
- Register a **Teams Channel** and paste Copilot’s public webhook (ngrok / reverse proxy).

### 3. Microsoft Teams  
- Upload Copilot’s `manifest.zip` via Teams Admin Center or sideload (Developer Preview).
- Free “Community” tenants do **not** support custom bots.

### 4. PostgreSQL  
- Stores every message, summary & checkpoint so Copilot can resume after restarts.
- Point Copilot to your existing Airflow DB **or** use the Docker‑Compose Postgres service or any persistent server database (such as RDS).
- Schema is created automatically on first run.

### 5. Ngrok Authtoken *(optional – use for local deployment only)*  
Need to expose Copilot’s local API URL to Azure Bot? Grab your personal Ngrok **authtoken**:

1. Sign in—or create a free account—at [ngrok.com](https://dashboard.ngrok.com/login).
2. Navigate to **☰ → Auth → Your Authtoken** in the sidebar.
3. Copy the token and use it in your `docker-compose` file.

---

## 🔗 Next Steps

- ➡️ **[Create an Azure Bot (for Microsoft Teams)](/quickstart/azure_bot/)**  
  Step‑by‑step Portal & CLI guide (single‑tenant vs multi‑tenant tips).

- ➡️ **[Upload Airflow Copilot App to Microsoft Teams](quickstart/prerequisites.md#upload-to-teams)**  
  Sideload or publish Copilot to your organisation.

> 💡 **Tip:** Run everything locally with Docker Compose for testing, then move the same containers to Kubernetes / ECS for production — just keep the environment variables consistent.
