
# 🐳 Airflow-Copilot Docker Usage Guide

This guide explains how to run the **Airflow Copilot** using Docker.

The **Airflow Copilot** is a GenAI-powered assistant that interacts with Apache Airflow environments. You can run it easily using Docker, either locally or in the cloud.

For in-depth configuration and deployment instructions, refer to:
- 📘 [Getting Started Guide](https://airflow-copilot.thedatacarpenter.com/quickstart/getting_started)
- 🛠️ [Deployment Guide](https://airflow-copilot.thedatacarpenter.com/deployment/deployment)

---

## 📦 Pull the Docker Image

```bash
docker pull thedatacarpenter/airflow-copilot:<version>
```

```bash
docker pull thedatacarpenter/airflow-copilot:latest
```

---

## 🚀 Run the Copilot

```bash
docker run --rm -p 3978:3978 thedatacarpenter/airflow-copilot:latest
```

---

## ⚙️ Required Environment Configuration

The container requires several environment variables, categorized below:

### 🔮 LLM Provider (pick one)

```env
LLM_MODEL_PROVIDER_NAME=OpenAI
LLM_MODEL_NAME=gpt-4o
OPENAI_API_KEY=your-openai-api-key
```

Other providers:
```env
GOOGLE_GENAI_API_KEY=ai-...
ANTHROPIC_API_KEY=ai-...
GROQ_API_KEY=ai-...
```

### 🤖 Azure Bot + Service Principal

```env
MICROSOFT_APP_ID=your-bot-id
MICROSOFT_APP_PASSWORD=bot-secret
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-spn-secret
AZURE_TENANT_ID=your-tenant-id
RESOURCE_GROUP=your-resource-group
```

### 🌐 Airflow REST API

```env
AIRFLOW_BASE_URL=http://localhost:8080/
AIRFLOW_AUTH_STRATEGY=per_user
```

### 🐘 Postgres DB

```env
DB_URI=postgresql://<user>:<password>@<host>:<port>/<database>
```

### 🔐 Security

```env
FERNET_SECRET_KEY=your-fernet-secret-key
```

Generate with:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 💬 Conversation Summarization

```env
MIN_MSG_TO_RETAIN=10
MIN_MSG_TO_SUMMARIZE=10
SUMMARIZATION_LLM_MODEL_PROVIDER_NAME=OpenAI
SUMMARIZATION_LLM_MODEL_NAME=gpt-4o
```

### 🌍 Optional: Ngrok for Local Development

```env
NGROK_AUTHTOKEN=your-ngrok-authtoken
```

---

## 🧪 Example: Run with Environment

```bash
docker run -p 3978:3978   -e LLM_MODEL_PROVIDER_NAME=OpenAI   -e LLM_MODEL_NAME=gpt-4o   -e OPENAI_API_KEY=your-key   -e AIRFLOW_BASE_URL=http://localhost:8080   -e FERNET_SECRET_KEY=your-secret   thedatacarpenter/airflow-copilot:latest
```

---

## 📍 Hosting the Docs

👉 [https://airflow-copilot.thedatacarpenter.com](https://airflow-copilot.thedatacarpenter.com/)

---

## ✅ Next Steps

- [Explore Deployment Options](https://airflow-copilot.thedatacarpenter.com/deployment/deployment)
- [Understand Auth Config](https://airflow-copilot.thedatacarpenter.com/architecture/airflow_auth_type)
- [Add Your Own Tools](https://airflow-copilot.thedatacarpenter.com/architecture/supported_apis)
