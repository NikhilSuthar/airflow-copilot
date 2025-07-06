
# 🚀 Production Deployment — Kubernetes Setup for Airflow Copilot

This guide covers how to deploy **Airflow Copilot** for production using **Kubernetes**, **Azure Bot Service**, and a cloud-hosted **PostgreSQL** database. It is a hardened and scalable alternative to the local Docker + ngrok setup.

---

## 🗺️ Architecture Overview

| Aspect            | **Local (Dev)**                                   | **Production (K8s)**                              |
|-------------------|---------------------------------------------------|---------------------------------------------------|
| Orchestrator      | Docker Compose                                    | Kubernetes (Deployment / StatefulSet)             |
| Public URL        | Ngrok tunnel                                      | Ingress / LoadBalancer                            |
| Storage backend   | Docker‑volume Postgres (ephemeral)                | Managed DB (RDS, CloudSQL) or in‑cluster StatefulSet |
| Scaling           | Single container                                  | Horizontal Pod Autoscaler (HPA)                   |
| Secrets           | `.env` file                                       | Kubernetes Secrets (sealed or external vault)     |
| Logging           | Container logs                                    | Centralised (ELK / Loki / CloudWatch)             |

---

### 📦 Production Architecture (conceptual)

![Production Deployment](../assets/production-docker-arch.svg)

- Airflow and Copilot run as independent pods in Kubernetes.
- Azure Bot Service sends messages to a public FastAPI endpoint (deployed via Ingress/LoadBalancer).
- PostgreSQL stores conversation states and summaries (hosted e.g., on RDS, CloudSQL, or Azure Database for PostgreSQL).
- Supported LLMs: OpenAI, Gemini (Google), Anthropic, Groq.

---

## 🧰 Prerequisites

- Azure Bot App + Teams Channel (must point to public endpoint)
- PostgreSQL (Cloud-hosted or managed DB)
- Kubernetes Cluster (AKS, GKE, EKS, or Minikube for testing)
- Docker Registry (GHCR, DockerHub, etc.)
- TLS certificate (optional but recommended for production)
- Domain for HTTPS endpoint (optional but ideal)
- Prepared `.env` values as Kubernetes secrets (see below)

---

## 📦 Kubernetes Resources

You need the following manifests:

### 1. Deployment (FastAPI + Copilot Agent)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-copilot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: copilot
  template:
    metadata:
      labels:
        app: copilot
    spec:
      containers:
        - name: copilot
          image: thedatacarpenter/airflow-copilot:latest
          ports:
            - containerPort: 3978
          envFrom:
            - secretRef:
                name: copilot-env
```

### 2. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: copilot-service
spec:
  type: ClusterIP
  selector:
    app: copilot
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3978
```

### 3. Ingress (Optional with cert-manager)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: copilot-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  rules:
    - host: copilot.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: copilot-service
                port:
                  number: 80
  tls:
    - hosts:
        - copilot.yourdomain.com
      secretName: copilot-tls
```

---

## 🔐 Secrets Management

Create Kubernetes secret with required environment variables:

```bash
kubectl create secret generic copilot-env   --from-literal=GOOGLE_GENAI_API_KEY=...   --from-literal=OPENAI_API_KEY=...   --from-literal=FERNET_SECRET_KEY=...   --from-literal=DB_URI=postgresql://...   --from-literal=MICROSOFT_APP_ID=...   --from-literal=MICROSOFT_APP_PASSWORD=...   --from-literal=MICROSOFT_APP_TENANT_ID=...   --from-literal=AZURE_CLIENT_ID=...   --from-literal=AZURE_CLIENT_SECRET=...
```

> 💡 Tip: You can also use Sealed Secrets, HashiCorp Vault, or AWS/GCP secret managers for more secure secret handling.

---

## 🛠️ Bot Endpoint Update

Ensure Azure Bot is updated with the **public HTTPS endpoint** of your Copilot FastAPI service (e.g. `https://copilot.yourdomain.com`). You can update this manually via Azure Portal or automate via a script.

---

## 🚨 Best Practices

- Enable autoscaling on Kubernetes based on CPU or memory.
- Use persistent cloud PostgreSQL for data durability.
- Mount volumes for logs or debugging if required.
- Use observability tools like Prometheus/Grafana for metrics.

---

## ✅ Final Notes

- No ngrok or localhost-based tunnels required in production.
- You can use cloud DNS for routing Azure Bot to Copilot API.
- Copilot persists conversation summaries for continuity.
- All Airflow interactions happen over REST API.
