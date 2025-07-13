# ---------- 1️⃣ Base Image ----------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# ---------- 2️⃣ Optional Azure CLI ----------
ARG INSTALL_AZURE_CLI=true

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
# ---------- 3️⃣ Python Deps ----------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- 4️⃣ App Code ----------
COPY src/ ./src
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# ---------- 5️⃣ Support Scripts ----------
COPY docker/scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

# ---------- 6️⃣ Entrypoint ----------
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn", "src.airflow_copilot.app.app:app", "--host", "0.0.0.0", "--port", "3978"]
