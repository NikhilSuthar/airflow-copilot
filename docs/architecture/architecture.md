# 🏗️ Airflow Copilot Architecture

## Overview

**Airflow Copilot** is designed to bridge **Microsoft Teams** with **Apache Airflow**, enabling conversational orchestration of DAGs and metadata management through a chatbot interface. It leverages **Azure Bot Services**, a LangGraph-based **AI Agent**, and native Airflow REST APIs to carry out intelligent, context-aware operations.

---

![Architecture Diagram](../assets/Standard-Architecture.svg)

---

The above diagram represents the **standard deployment architecture** of Airflow Copilot. All components inside the **green dotted box** can be deployed locally or on the cloud.

On cloud environments, the system can run as a single **Dockerized application** or be designed using **serverless architecture** principles.

Refer to the **Deployment section** for environment-specific setup details.

---

## 🔁 Components

| Component               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Microsoft Teams**     | The user interface where individuals interact with the Copilot chatbot.     |
| **Airflow Copilot Bot** | Custom chatbot app hosted on the Microsoft Teams framework.                 |
| **Azure Bot Service**   | Routes messages securely via HTTPS to the registered bot webhook.           |
| **Bot API Layer**       | The FastAPI application that receives messages and triggers agent logic.    |
| **Bot Adapter**         | Bridges communication between the API layer and the AI Agent.               |
| **Airflow Copilot Agent** | LangGraph-based agent that handles stateful conversations and tool logic. |
| **PostgreSQL**          | Persists conversation state and user metadata.                              |
| **Apache Airflow**      | The orchestrator under automation, accessed via its native REST API.        |

---

## 🌐 Network Topology

| Direction  | Protocol | Source                    | Target                   | Description                                                  |
|------------|----------|---------------------------|--------------------------|--------------------------------------------------------------|
| Inbound    | HTTPS    | Azure Bot Service         | FastAPI Webhook          | Delivers user activity to the Airflow Copilot backend.       |
| Internal   | Local    | FastAPI (Bot API Layer)   | Bot Adapter              | Normalizes messages and state for the agent.                 |
| Internal   | LangGraph| Bot Adapter               | Airflow Copilot Agent    | Executes conversation flow and tools via LangGraph.          |
| Outbound   | HTTPS    | Airflow Copilot Tools     | Apache Airflow REST API  | Triggers DAGs, retrieves logs, manages metadata/configs.     |

---

## 🔒 Security

- **Azure Bot Identity**: Manages secure identity and session routing via Microsoft.
- **Encrypted HTTPS Webhook**: All communication between Teams and the bot is encrypted.
- **Credential Encryption**: Per-user Airflow credentials are encrypted using a **Fernet key** and stored securely in **PostgreSQL**.
- **Access Control**: Supports both centralized and per-user credential modes to enforce fine-grained access control on Airflow.

---

## 🔄 Deployment Flexibility

- Local development supported via **ngrok** for HTTPS tunneling.
- One-step **Docker Compose** setup for FastAPI, PostgreSQL, and optional Airflow container.
- Compatible with **Azure**, **AWS**, **GCP**, or any **Kubernetes / VM** deployment model.
- Easily extensible to Slack, Web App UIs, or other messaging platforms via the Bot Adapter.

---


## 🔗 Next Steps

- **[Agent workflow](../agent)**: Understand the Agent workflow.
- **[Message Summarization](../summarization)**: Understand the Agent workflow.
- **[Supported Airflow Copilot Features](../supported_apis)**: List of activity Airflow copilot can do.


> 💡 **Pro Tip:** To fully unlock the agent's capabilities, pair it with summarization, memory retention, and message pruning for production-scale deployments.

