# ---------- 1️⃣ Base Image ----------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# ---------- 2️⃣ Optional Azure CLI ----------
ARG INSTALL_AZURE_CLI=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl ca-certificates && \
    if [ "$INSTALL_AZURE_CLI" = "true" ]; then \
      apt-get install -y --no-install-recommends gnupg2 software-properties-common && \
      curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | \
        gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg && \
      echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] \
        https://packages.microsoft.com/repos/azure-cli/ bullseye main" \
        > /etc/apt/sources.list.d/azure-cli.list && \
      apt-get update && \
      apt-get install -y --no-install-recommends azure-cli && \
      apt-get purge --auto-remove -y gnupg2 software-properties-common && \
      rm -rf /var/lib/apt/lists/*; \
    else \
      echo "⏭️ Skipping Azure CLI install"; \
    fi

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
