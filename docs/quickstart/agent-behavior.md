# 🚨 Behavior Notes & Known Limitations

This document outlines key behavior details, recommendations, and known limitations of the Airflow Copilot agent to help you understand how it operates and what to expect during usage.

## 🔍 Important Behavior Notes

- **Airflow Version Support:**
  Airflow Copilot is designed around the Airflow **2.5.1 REST API**. While most functionality works across versions **2.5 to 2.11**, some **latest API endpoints introduced in newer versions may not be supported yet.**

- **Large API Responses & Token Limits:**
  Airflow REST responses, especially for DAG runs and task logs, can be **very large**. This may cause token overflows when using models with strict limits (such as free model on `Groq`). We recommend using robust providers like **OpenAI** or **Google AI** for better handling of large responses.

- **User Creation Behavior:**
  The Copilot supports **creating new users and assigning roles**. However, if a password is **not provided**, it generates one automatically. Depending on model behavior, the password **may or may not be returned** reliably in the response.

- **First-Time Slowness & History Refresh:**  
  The assistant might respond slowly in some cases, especially when multiple backend API calls are involved.  
  It is highly recommended to give tasks **one by one** instead of combining them.  

    **For example:** Instead of asking _"Create a user named as Matt and assign a role with only permission to X DAG"_ in a single prompt, break it down into steps:

      1. Ask it to **create the user Matt with email .... and password ....**  
      2. Then ask it to **create a custom role**  
      3. Finally, ask it to **assign that role to the user**

- **Trust but Verify:**
  Occasionally, the AI may claim that an action (e.g., disabling a DAG) was performed, even if it wasn’t successful. Always **verify critical actions** by asking the Copilot for confirmation (e.g., "Is DAG `xyz` disabled?").

- **Message Timing:**
  Avoid sending multiple messages back-to-back. Wait for the assistant to respond, as it begins processing immediately after receiving input. **Sending too many messages at once may confuse the context**.

- **Recommended Practice: Refresh History:**
  Before starting a new task or conversation, it is a good practice to **refresh history** so that the assistant has the relevant context available.

---

## 🚫 Known Limitations

- **Only Microsoft Teams as Channel Support:**
  Current version of copilot only support conversion through Microsoft Teams. In futher there will be more channel will be added.

- **DAG Deletion Not Supported:**
  For safety reasons, Copilot **does not support DAG deletion**. It will recommend **disabling DAGs instead**.

- **Changing DAG Schedule or Tags:**
  The Airflow REST API does **not currently support updating DAG schedule intervals or tags**. As a workaround, you can use **Airflow Variables** in your DAG code to define the schedule, and let Copilot update the variable value to reflect the change.

- **Only v1 API Used:**
  Copilot uses only the **v1 REST API**. Airflow's v2 API is not yet supported.

- **Partial Compatibility with Older Versions:**
  While Copilot works well with versions **2.5 to 2.11**, some features may behave differently or be **partially supported** on older versions.

- **Work well with Specific Information:**
  While Copilot works well most of the cases but still if the volume of your Airflow  is high such total number of dags are more than 50 then it will be good to provide the proper name such as dag_id or run time etc to make it more effective.
---

> 📝 If you encounter inconsistent behavior, especially on older Airflow versions or with custom setups, consider submitting feedback or filing an issue to help us improve.
