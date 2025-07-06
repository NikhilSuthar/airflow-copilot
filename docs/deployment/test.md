
# 🚀 Production Deployment — Airflow Copilot on Kubernetes & Docker Compose

This guide shows two production‑grade deployment paths:

1. **Kubernetes** (AKS / EKS / GKE) – scalable and cloud‑native.  
2. **Docker Compose (VM / bare metal)** – simple, one‑host prod.

Both share a **single `.env` file** for environment variables so you define secrets **once** and reuse them everywhere.

---

## 1 — Directory Layout

```txt
repo-root/
├─ .env                       # all sensitive vars
├─ docker-compose.prod.yml    # VM / staging deployment
└─ k8s/                       # Kubernetes manifests
```

---

## 2 — `.env` Template (example)

```dotenv
# LLM
LLM_MODEL_PROVIDER_NAME=OpenAI
LLM_MODEL_NAME=gpt-4o
OPENAI_API_KEY=sk-...

# Azure Bot / SPN
MICROSOFT_APP_ID=XXXXXXXX-...
MICROSOFT_APP_PASSWORD=bot-secret
MICROSOFT_APP_TENANT_ID=XXXXXXXX-...
AZURE_CLIENT_ID=XXXXXXXX-...
AZURE_CLIENT_SECRET=spn-secret

# Postgres
DB_URI=postgresql://user:pass@pg.example.com:5432/copilot

# Airflow
AIRFLOW_BASE_URL=https://airflow.example.com/api/v1

# Misc
FERNET_SECRET_KEY=base64-32-byte-key
```

> 💡 **Keep `.env` outside VCS** (`.gitignore`). Use a secrets manager for prod.

---

## 3 — Production Docker Compose (`docker-compose.prod.yml`)

```yaml title="docker-compose.prod.yml"
version: "3.9"

services:
  copilot:
    image: thedatacarpenter/airflow-copilot:1.0.0
    restart: unless-stopped
    env_file: .env            # ⬅️ load all vars
    ports:
      - "3978:3978"
    depends_on: [db-init]

  db-init:
    image: postgres:16        # only psql client
    env_file: .env
    entrypoint: ["/bin/bash","/init_db.sh"]
    restart: "no"
```

Run:

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

## 4 — Kubernetes Manifests (reuse `.env`)

### 4.1 Create secrets directly from `.env`

```bash
kubectl create namespace copilot
kubectl -n copilot create secret generic copilot-env --from-env-file=.env
```

### 4.2 Core Manifests

<details>
<summary><code>k8s/10-copilot.yaml</code></summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: copilot
  namespace: copilot
spec:
  replicas: 2
  selector:
    matchLabels: { app: copilot }
  template:
    metadata:
      labels: { app: copilot }
    spec:
      containers:
        - name: copilot
          image: thedatacarpenter/airflow-copilot:1.0.0
          ports: [{ containerPort: 3978 }]
          envFrom:
            - secretRef: { name: copilot-env }
          readinessProbe:
            httpGet: { path: /ready, port: 3978 }
            initialDelaySeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: 3978 }
            initialDelaySeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: copilot-svc
  namespace: copilot
spec:
  selector: { app: copilot }
  ports:
    - port: 80
      targetPort: 3978
```
</details>

<details>
<summary><code>k8s/20-ingress.yaml</code></summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: copilot-ingress
  namespace: copilot
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts: ["copilot.example.com"]
      secretName: copilot-tls
  rules:
    - host: copilot.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: copilot-svc
                port: { number: 80 }
```
</details>

Apply:

```bash
kubectl apply -f k8s/
```

---

## 5 — Update Azure Bot Endpoint

Point messaging endpoint → `https://copilot.example.com/api/messages`.

---

## 6 — Best‑Practice Checklist

| Domain | Recommendation |
|--------|----------------|
| **TLS** | Use cert‑manager or pre‑issued certs for HTTPS |
| **Scaling** | `kubectl autoscale deploy copilot -n copilot --cpu-percent=70 --min=2 --max=10` |
| **Backups** | Enable automated snapshots on managed Postgres |
| **Observability** | Scrape `/metrics`, forward logs to Loki/ELK |
| **Secrets** | Rotate regularly, store in vault / Sealed Secrets |

---

## ✅ You’re Live

- **Compose**: Copilot running on port `3978` behind your own Nginx/Traefik.  
- **Kubernetes**: Ingress HTTPS endpoint ready for Teams.  
- **One `.env`** powers both—converted to K8s secrets with a single command.

Happy automating! 🎉
