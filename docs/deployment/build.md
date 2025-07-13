# 🛠️ Build & Publish Docker Image for Airflow Copilot

This guide explains how to build  [Airflow Copilot](https://thedatacarpenter.com/airflow-copilot), locally.

---

## 📦 What's in the Docker Image?

The Docker image includes:

- A FastAPI web server that runs the Copilot agent
- LangGraph agent with integrated tools
- Optional SQL file for database bootstrapping
- Microsoft Teams bot integration
- Secure environment variable support

---

## 🧰 Prerequisites

Ensure the following are installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/downloads)
- DockerHub or any container registry account

---

## 🪜 Step-by-Step Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/NikhilSuthar/airflow-copilot.git
cd airflow-copilot
```

---

### 2️⃣ Configure the `.env` File

Copy the example env file:

```bash
cp .env.example .env
```

Then edit `.env` with your values:

```env
LLM_MODEL_PROVIDER_NAME=openai
LLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=your_openai_key
MICROSOFT_APP_ID=your_app_id
MICROSOFT_APP_PASSWORD=your_password
DB_URI=postgresql+psycopg2://user:pass@host:port/dbname
FERNET_SECRET_KEY=your_fernet_key
```

---


### 3️⃣ change the `docker-compose.loca.yml` file

Update the image tag to build tag in `docker-compose.local.yml` file.
Replace below 

```bash
    image: thedatacarpenter/airflow-copilot:latest
```

with 

```bash
    build:
      context: .
      dockerfile: Dockerfile
```

### 4️⃣ Local Run (Test)
Use below command to build and run

```bash
    docker compose -f docker-compose.local.yml  up --build --force-recreate
```

### 4️⃣ Stop 
Press `ctrl+c` and enter below command:

```bash
    docker compose -f docker-compose.local.yml  down -v
```



---


---

## 📦 Download

To download the pre-built image:

```bash
docker pull thedatacarpenter/airflow-copilot:latest
```

To use this image in Docker Compose:

```yaml
services:
  copilot:
    image: thedatacarpenter/airflow-copilot:latest
    ports:
      - "3978:3978"
    env_file: .env
```

---

## ✅ Done!

You now have a production-ready Docker image of Airflow Copilot.

> 🔄 Rebuild & re-push the image every time you make source code changes.

For deployment options (Docker, AWS, Azure), see the full [Deployment Guide](./deployment.md).

---