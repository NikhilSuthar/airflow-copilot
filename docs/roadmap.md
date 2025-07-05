# 🔭 Product Roadmap

This page outlines the upcoming features and long-term vision for **Airflow Copilot**. While the current version offers powerful orchestration capabilities via Microsoft Teams, several enhancements are actively being explored to make the assistant more intelligent, proactive, and versatile.

---

## 🧠 Planned Enhancements

### 1. 🔧 Tooling Optimization
Improve the performance and accuracy of existing tools used by the AI agent—especially around error handling, fallback mechanisms, and dynamic Airflow version support.

### 2. 🗄️ Redis Support as Copilot Backend

Introduce **Redis** as an optional backend for storing Copilot state, checkpoints, and intermediate responses. This addition aims to:

- Enhance performance for high-concurrency environments.
- Reduce latency during message summarization and session context recall.
- Support distributed deployments with better scalability.
- Serve as an alternative to PostgreSQL for ephemeral state tracking.

> 💡 Redis will be especially useful in stateless serverless deployments or scenarios where conversation history doesn't need long-term persistence.


### 3. 📡 Multi-Channel Communication
Expand Copilot’s availability to support other messaging platforms beyond Microsoft Teams (e.g., Slack, Discord, Webchat). This ensures greater accessibility for users across teams and infrastructures.

### 4. 🔔 Proactive Monitoring (User-Driven)
Introduce intent-based monitoring. Example:
> _“Copilot, monitor `my_dag` tonight and notify me if it fails.”_

Copilot will intelligently track execution outcomes and proactively notify the user based on specific instructions.

### 5. ✉️ Email Notification Integration
Enable direct email support for DAG status updates, alerts, and action confirmations. This allows users to receive updates even outside their chat interface.

---

## 💡 Have a Feature Request?

I'd love to hear from you! Feel free to open a [GitHub issue](https://github.com/your-repo/issues) or suggest improvements via your preferred channel.

---

> ℹ️ Note: Roadmap items are subject to change based on user feedback, platform limitations, and emerging use cases. Stay tuned for updates!
