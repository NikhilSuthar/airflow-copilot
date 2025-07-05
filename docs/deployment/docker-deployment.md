# 📦 Airflow Copilot – Deployment Guide

Run Copilot in production with durable storage, secrets management, and automated upgrades.

* **Quick links:** [Architecture](#1-architecture) · [Docker Compose](#2-production-compose-file) · [Publishing images](#3-publishing-a-new-image) · [Security](#4-security-best-practices) · [Scaling](#5-scaling--observability)

---

## 1. Architecture

```
copilot ──▶ Airflow API
   │
   ├─▶ Postgres  (conversation store)
   └─▶ Redis*    (optional caching)

ngrok*  ─▶ public URL → Azure Bot Framework  
*optional in development
```

---

## 2. Production Compose file

Create `docker-compose.yml` and keep it under version control (**without** secrets).

```yaml
version: "3.9"

volumes:
  pgdata:

services:
  copilot:
    image: <your-dockerhub-username>/airflow-copilot:1.2.0  # pin an exact tag
    restart: unless-stopped
    user: "1001:1001"               # non‑root
    env_file:                       # store secrets outside Git
      - copilot.env
    ports:
      - "3978:3978"
    depends_on:
      - postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3978/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3

  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: lang_memory
    volumes:
      - pgdata:/var/lib/postgresql/data

  # --- Development‑only: expose Copilot on the internet ---
  ngrok:
    image: ngrok/ngrok:latest
    command: http copilot:3978
    environment:
      NGROK_AUTHTOKEN: ${NGROK_AUTHTOKEN}
    ports:
      - "4040:4040"

  # --- Automatically update Azure Bot endpoint when ngrok URL changes ---
  bot-updater:
    image: <your-dockerhub-username>/airflow-copilot:1.2.0
    entrypoint: ["/usr/local/bin/update_bot.sh"]
    depends_on:
      - ngrok
    environment:
      NGROK_API: http://ngrok:4040/api/tunnels
      AZURE_CLIENT_ID: ${MICROSOFT_APP_ID}
      AZURE_CLIENT_SECRET: ${MICROSOFT_APP_PASSWORD}
      AZURE_TENANT_ID: ${MICROSOFT_APP_TENANT_ID}
      AZURE_SUBSCRIPTION_ID: ${AZURE_SUBSCRIPTION_ID}
      BOT_NAME: AirflowCopilot
      RESOURCE_GROUP: my-rg
```

### `copilot.env` (template)

```
# LLM
LLM_MODEL_PROVIDER_NAME=Google_GenAi
LLM_MODEL_NAME=gemini-2.5-flash
GOOGLE_GENAI_API_KEY=<api key>

# Database
DB_URI=postgresql://airflow:airflow@postgres:5432/airflow

# Airflow
AIRFLOW_BASE_URL=http://host.docker.internal:8080/api/v1
AIRFLOW_AUTH_STRATEGY=centralized
AIRFLOW_USER_NAME=airflow
AIRFLOW_USER_PASSWORD=airflow

# Azure Bot
MICROSOFT_APP_ID=<...>
MICROSOFT_APP_PASSWORD=<...>
MICROSOFT_APP_TENANT_ID=<...>

# Copilot summarisation
MIN_MSG_TO_SUMMARIZE=10
MIN_MSG_TO_RETAIN=10
FERNET_SECRET_KEY=<32-byte-base64>
```

---

### Launch

```bash
docker compose pull          # fetch latest images
docker compose up -d         # start in detached mode
```

Check health:

```bash
docker compose ps
docker compose logs -f copilot
```

---

## 3. Publishing a new image (maintainers)

```bash
docker build -t airflow-copilot .
docker tag   airflow-copilot <your-dockerhub-username>/airflow-copilot:1.2.0
docker push  <your-dockerhub-username>/airflow-copilot:1.2.0
```

---

## 4. Security best practices

| Area | Recommendation |
|------|----------------|
| **Secrets** | Store in `.env`, Docker secrets, or a vault – never in Git. |
| **TLS** | Terminate HTTPS via Traefik/Nginx in front of Copilot. |
| **User IDs** | Run containers as non‑root (`user: "1001:1001"`). |
| **Upgrades** | Pin image tags, track CVEs, and rebuild when base images patch. |
| **Backups** | Snapshot Postgres volume or enable WAL archiving. |

---

## 5. Scaling & observability

* **Horizontal scaling** – stateless replicas behind a load balancer (state in Postgres).  
* **Metrics** – Prometheus‑friendly endpoint at `/metrics` (port 3979).  
* **Logs** – JSON to stdout; route to Fluentd, Loki, or Elastic.  
* **Autoscaling** – KEDA with custom metrics or CPU threshold.

---

## 6. Troubleshooting

| Symptom | Possible fix |
|---------|--------------|
| `HTTP 401` from Airflow | Verify `AIRFLOW_AUTH_STRATEGY` and credentials. |
| Slow responses | Increase Gunicorn workers (`GUNICORN_WORKERS=4`). |
| “Tunnel not found” in bot updater | Ensure `ngrok` is healthy and port 3978 is exposed. |

---

### Useful links

* Azure Bot channel registration → <https://learn.microsoft.com/azure/bot-service/>  
* Airflow REST API reference → <https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html>
