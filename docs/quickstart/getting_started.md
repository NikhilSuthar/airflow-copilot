# 🚀 Getting Started — Airflow Copilot  

This guide walks you through launching  **Airflow Copilot** using Docker Compose files.

---

## 🧰 Prerequisites

Make sure you have the following ready:

- **Docker** – Install from [**Docker Docs**](https://docs.docker.com/engine/install/)
- **Apache Airflow** – Version `2.5.0` to `< 3.0.0`  
  Use the [official Docker Compose setup](https://airflow.apache.org/docs/apache-airflow/2.11.0/howto/docker-compose/index.html)
- **PostgreSQL** – Shared between Airflow and Copilot
- **Ngrok Authtoken** – For public URL tunneling (local bot testing)
- **Azure Bot Credentials** – follow [Create an Azure Bot](/quickstart/azure_bot/) to obtain  
    - Microsoft App ID & Password  
    - Azure Service Principal (Client ID & Secret)  
    - Azure Resource Group  
    - Azure Tenant ID
- **Fernet Key** (32‑byte secret): create using below script (if not)

  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```

- **LLM Provider & API Keys**  
    Supported: `OpenAI`, `Google_GenAI`,  `Anthropic`

    To get started with Google Gemini, [**create a free API key**](https://ai.google.dev/) and use the `gemini-2.5-flash` model.


---

> **Note:** This Quick Start guide covers local deployment only. For production or cloud-based deployments, refer to the [**Deployment**](/deployment/docker-deployment) section.


## 🛠 Step 1 — Launch Apache Airflow

If Airflow isn’t running:

1. Follow the guide: [**Run Airflow via Docker Compose**](https://airflow.apache.org/docs/apache-airflow/2.11.0/howto/docker-compose/index.html)
2. Ensure Airflow and PostgreSQL are up.

➡️ Airflow UI → <http://localhost:8080>  
🔐 Login → `admin` / `admin`

---

## 🤖 Step 2 — Deploy Airflow Copilot

1. Create **`docker-copilot-compose.yml`** in.  
2. Copy the YAML below.  
3. Replace **`${PLACEHOLDERS}`** with real values.
4. If you have created a **Service Principal** for your Azure Bot, you can reuse the same credentials:  
    - Set `MICROSOFT_APP_ID` as `AZURE_CLIENT_ID`  
    - Set `MICROSOFT_APP_PASSWORD` as `AZURE_CLIENT_SECRET`  
   
    For detailed steps, refer to the [**Create Azure Bot**](../quickstart/azure_bot.md) section.



📘 Variable reference → [**Environment Variables**](../configuration/environment_variables.md)

Create below file.

### `docker-copilot-compose.yml`

```yaml
version: "3.9"

services:
  copilot:
    build: .
    container_name: copilot
    restart: unless-stopped
    depends_on: [db-init]
    ports: ["3978:3978"]
    environment:
      LLM_MODEL_PROVIDER_NAME: [Google_Genai|OpenAI|Anthropic]
      LLM_MODEL_NAME: ${LLM_MODEL_NAME}
      GOOGLE_GENAI_API_KEY: ${GOOGLE_GENAI_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}

      DB_URI: postgresql://airflow:airflow@host.docker.internal:5432/airflow?sslmode=disable

      MICROSOFT_APP_ID: ${MICROSOFT_APP_ID}
      MICROSOFT_APP_PASSWORD: ${MICROSOFT_APP_PASSWORD}
      MICROSOFT_APP_TENANT_ID: ${MICROSOFT_APP_TENANT_ID}

      AIRFLOW_BASE_URL: http://host.docker.internal:8080/
      AIRFLOW_AUTH_STRATEGY: centralized
      AIRFLOW_USER_NAME: airflow
      AIRFLOW_USER_PASSWORD: airflow

      MIN_MSG_TO_SUMMARIZE: 10
      MIN_MSG_TO_RETAIN: 10
      FERNET_SECRET_KEY: ${FERNET_SECRET_KEY}
    networks: [airflow]

  db-init:
    image: postgres:16
    entrypoint: ["/bin/bash", "/init_db.sh"]
    restart: "no"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_URI: postgresql://airflow:airflow@host.docker.internal:5432/airflow?sslmode=disable
    volumes:
      - ./docker/scripts/init_db.sh:/init_db.sh:ro
      - ./docker/scripts/init.sql:/init.sql:ro
    networks: [airflow]

  ngrok:
    image: ngrok/ngrok:latest
    depends_on: [copilot]
    command: http copilot:3978 --log stdout
    environment:
      NGROK_AUTHTOKEN: ${NGROK_AUTHTOKEN}
    ports: ["4040:4040"]
    networks: [airflow]

  bot-updater:
    build: .
    depends_on: [ngrok]
    entrypoint: ["/usr/local/bin/update_bot.sh"]
    restart: "no"
    environment:
      NGROK_API: http://ngrok:4040/api/tunnels
      BOT_NAME: Airflow-Copilot
      RESOURCE_GROUP: my-rg
      AZURE_CLIENT_ID: ${AZURE_CLIENT_ID}
      AZURE_TENANT_ID: ${AZURE_TENANT_ID}
      AZURE_CLIENT_SECRET: ${AZURE_CLIENT_SECRET}
    networks: [airflow]

volumes:
  pgdata:

networks:
  airflow:
    driver: bridge
```

---

## ▶️ Run Copilot

```bash
# Create Docker network (once)
docker network create airflow

# Start all services
docker compose -f docker-copilot-compose.yml up -d
```

---

## 🧽 Clean Up

```bash
docker compose -f docker-copilot-compose.yml down -v
```

---

### What Happens Next 🎉

- Copilot launches on **`http://localhost:3978`**  
- Ngrok exposes a public URL and the Azure bot endpoint is patched automatically  
- Chat with **Airflow Copilot** directly in Microsoft Teams! Login to Azure Portal and validate the same.

![Azure Bot Message Endpoint](../assets/Message-Endpoint-Bot.png)

