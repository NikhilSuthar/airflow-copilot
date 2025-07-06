
# 🚀 Airflow Copilot — Deployment Modes Overview

This guide compares the three deployment options for **Airflow Copilot**:

1. 🧪 Local Development (Docker + Ngrok)
2. 🧱 Docker-based Production Deployment
3. ☁️ Kubernetes-based Cloud Deployment

> **Note:** The following sections assume you’ve already completed [**Azure Bot creation**](../quickstart/azure_bot.md) and [**installed the Copilot app in Microsoft Teams**](../quickstart/upload_app.md).


All options use the same `.env` file format for managing environment variables.

---

## 📊 Comparison Table

| Aspect                  | Local (Dev)                          | Docker (Prod)                         | Kubernetes (Prod)                      |
|-------------------------|--------------------------------------|---------------------------------------|----------------------------------------|
| Deployment Method       | Docker Compose                       | Docker Compose                        | Kubernetes YAML manifests              |
| Public Access           | Ngrok Tunnel                         | Reverse Proxy (e.g., NGINX)            | Ingress / LoadBalancer + DNS           |
| Bot Endpoint Setup      | Auto-patched via `update_bot.sh`     | Manual or scripted                    | Manual or scripted                      |
| PostgreSQL              | Host or Container DB (ephemeral)     | External DB (e.g., RDS)                | Cloud-hosted DB or StatefulSet         |
| TLS/HTTPS               | Via Ngrok                            | Setup via NGINX                       | TLS via cert-manager                   |
| Secrets Management      | `.env` file                          | `.env` file                           | Kubernetes Secrets                      |
| Scaling                 | Not applicable                       | Manual                                | HPA or KEDA                             |
| Logging & Monitoring    | Local stdout                         | Volume/log driver                     | Centralized (ELK / Prometheus / Grafana)|

---

## 🛠 Prepare Environment Variables

All deployment types rely on a single `.env` file. 

<details>
<summary><code>.env</code></summary>
```env
--8<-- "./.env.example"
```
</details>

---

# 1️⃣ Local Deployment (Docker + Ngrok)

- Recommended for development and testing.
- **Ngrok** exposes a public endpoint for Microsoft Teams.
- The `bot-updater` service automatically updates the Azure Bot messaging endpoint using Azure Service Principal.


##  **Architecture**

![Local Deployment](../assets/quick-start-arch.svg)

## **Steps:**
- Follow the full  [**Getting Started**](../quickstart/getting_started.md) guide.

---

# 2️⃣ Docker-Based Production Deployment

- Uses the same Copilot Docker image, but with a hardened **`.env`**.
- A reverse proxy like NGINX is used to expose the service over TLS.
- PostgreSQL must be externally hosted (e.g., RDS, Cloud SQL).
- Azure Bot messaging endpoint must be updated manually.

## Prerequisites (Docker Production)

In addition to the general requirements listed earlier, the following components are essential for deploying **Airflow Copilot** in a production environment using Docker Compose:

1. **Apache Airflow Instance**  
   - A running Airflow instance (version ≥ 2.5.0) with the REST API enabled and accessible to Copilot.

2. **Persistent PostgreSQL Database**  
   - A reliable PostgreSQL instance (self-hosted or managed, e.g., AWS RDS, Azure DB) to store conversation history and LangGraph checkpoints.

3. **Reverse Proxy (e.g., NGINX or Traefik)**  
   - Required to securely expose FastAPI (/api/messages) over HTTPS.  

> 💡 You may also want to integrate with a certificate manager like Let's Encrypt for automatic HTTPS.


##  **Architecture**

![Prod Docker](../assets/docker-prod-deployment.svg)

## **Steps:**

1. **Prepare `.env` file**: Populate your `.env` file with required values. Skip any variables that used only in local mode.  
Reference [**Environment Variables**](../configuration/environment_variables.md)

2. Create `docker-compose.prod.yml`

    <details>
    <summary><code>docker-compose.prod.yml</code></summary>
    ```yaml title="docker-compose.prod.yml"
    --8<-- "./docker-compose.prod.yml"
    ```
    </details>

3.  **Start Services**

    ```bash
    # Create Docker network (once)
    docker network create airflow

    # Start all services
    docker compose -f docker-compose.prod.yml up -d
    ```
4. **Expose via Reverse Proxy**: 
    
    Configure NGINX or similar to route `https://copilot.yourdomain.com/api/messages → http://copilot:3978`.  Then update your Azure Bot endpoint in the portal:

    ```bash
        https://copilot.yourdomain.com/api/messages
    ```
5. **You're Done !!!**

---

# 3️⃣ Kubernetes Deployment (Cloud)

- Ideal for enterprise-scale deployments.
- Public domain and TLS managed through Ingress + cert-manager.
- Environment variables passed securely as Kubernetes Secrets.


> See: [`production-deployment.md`](../deployment/production-deployment.md)

## Prerequisites (Kubernetes Production)

1. **Kubernetes Cluster**  
   - A working K8s cluster (e.g., AKS, EKS, GKE, or self-hosted).  
   - `kubectl` access with appropriate permissions to apply resources.

2. **Docker Registry Access**  
   - A container registry (e.g., Docker Hub, GHCR, ECR) to host and pull the Copilot Docker image.  
   - Ensure the image is pushed and accessible from within the cluster.

3. **Azure Bot App with Teams Channel**  
   - A registered Azure Bot with Microsoft App ID & Password.  
   - The bot’s messaging endpoint must point to your public Copilot Ingress URL.

4. **Cloud-hosted PostgreSQL (or StatefulSet)**  
   - A production-grade PostgreSQL instance (e.g., RDS, Cloud SQL) for storing Copilot state and summaries.  
   - Alternatively, deploy it as a StatefulSet inside Kubernetes with persistent volumes.

5. **Ingress Controller (e.g., NGINX)**  
   - Required to expose the Copilot FastAPI service publicly.  
   - Enables domain-based access and TLS termination.

6. **TLS Certificates (Recommended)**  
   - Use cert-manager with Let’s Encrypt to secure your public domain via HTTPS.  
   - Update the Azure Bot endpoint to use the secured URL.

7. **Secrets Management**  
   - Store sensitive environment variables as Kubernetes Secrets.  
   - Use sealed secrets, HashiCorp Vault, or native K8s secrets based on your security policy.

> 💡 All required configuration values (API keys, credentials, endpoints) should be declared in a shared `.env` file and converted to Kubernetes secrets during deployment.


## **Architecture**

![Kubernetes Deployment](../assets/production-docker-arch.svg)


## **Steps:**

1. **Prepare Environment Variables**: Create a **`.env`** file (as mentioned above) and populate it with the required environment variables. You may omit any variables that are specifically needed for local deployments only. For a complete reference, see [**Environment Variables**](../configuration/environment_variables.md) for variable details.

2. **Generate Kubernetes Secret**

    ```bash
        kubectl create namespace airflow-copilot
        kubectl -n airflow-copilot create secret generic airflow-copilot-env --from-env-file=.env
    ```
3. **Create Deployment Manifest**

    <details>
    <summary><code>airflow-copilot-deployment.yaml</code></summary>
    ```yaml title="airflow-copilot-deployment.yaml"
    --8<-- "./k8s/airflow-copilot-deployment.yaml"
    ```
    </details>

4. **Create Ingress (Optional)**

    <details>
    <summary><code>airflow-copilot-ingress.yaml</code></summary>
    ```yaml title="airflow-copilot-ingress.yaml"
    --8<-- "./k8s/airflow-copilot-ingress.yaml"
    ```
    </details>

5. **Apply All Resources**

    ```bash
        kubectl apply -n airflow-copilot -f airflow-copilot-deployment.yaml
        kubectl apply -n airflow-copilot -f airflow-copilot-service.yaml
        kubectl apply -n airflow-copilot -f airflow-copilot-ingress.yaml
    ```
7. **Update Azure Bot Endpoint**
    Update your Azure Bot messaging endpoint to the public URL exposed via Ingress:
    
        ```url
        https://airflow-copilot.yourdomain.com/api/messages
        
        ```
        See [**Azure Bot Setup**](../quickstart/azure_bot.md) for more details.
8. **You're Done !!!**
---
    

## 📦 Deployment Summary

| Mode       | Ideal For       | Public Endpoint     | DB Storage   |
|------------|-----------------|---------------------|--------------|
| Local      | Testing/dev     | Ngrok               | Host/local   |
| Docker     | Small teams     | Reverse Proxy/Nginx | Cloud DB     |
| Kubernetes | Enterprise Prod | DNS + TLS Ingress   | Managed DB   |
