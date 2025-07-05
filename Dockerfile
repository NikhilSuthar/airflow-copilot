# -------- 1️⃣ Base image + system deps ----------
FROM python:3.11-slim-bullseye

# Update system packages to latest versions to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 🔧 Install system tools (curl is needed!)
# 🔧 Install system tools and Azure CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      apt-transport-https \
      lsb-release \
      gnupg && \
    curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null && \
    AZ_REPO=$(lsb_release -cs) && \
    echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" \
      > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && \
    apt-get install -y azure-cli && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*


# -------- 2️⃣ Python deps ----------
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# -------- 3️⃣ App code ----------
COPY src/ ./src
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# -------- 4️⃣ Script ----------
COPY docker/scripts/update_bot.sh /usr/local/bin/update_bot.sh
RUN chmod +x /usr/local/bin/update_bot.sh
COPY docker/scripts/init_db.sh /usr/local/bin/init_db.sh
RUN chmod +x /usr/local/bin/init_db.sh
COPY docker/scripts/init.sql /usr/local/bin/init.sql
RUN chmod +x /usr/local/bin/init.sql
# -------- 5️⃣ Start app ----------
CMD ["uvicorn", "airflow_copilot.app.app:app", "--host", "0.0.0.0", "--port", "3978"]
