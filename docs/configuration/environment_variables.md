# ⚙️ Airflow Copilot – Environment Configuration

This document describes all the environment variables required for running **Airflow Copilot**, including their purpose, default values, and behavior across different authentication strategies.

---

## 🧠 Core Configuration

| Variable                          | Description                                                                 | Required | Default |
|----------------------------------|-----------------------------------------------------------------------------|----------|---------|
| `LLM_MODEL_PROVIDER_NAME`        | The name of the LLM provider (e.g., `openai`, `google_genai`)                       | ✅       | –       |
| `LLM_MODEL_NAME`                 | The specific model to use (e.g., `gpt-4`, `mixtral-8x7b`)                   | ✅       | –       |
| `{PROVIDER}_API_KEY`| API key used to authenticate with the selected LLM provider                | ✅       | –       |
| `DB_URI`                         | PostgreSQL URI for persisting agent state and user data                    | ✅       | –       |
| `MICROSOFT_APP_ID`              | Azure Bot App registration ID                                              | ✅       | –       |
| `MICROSOFT_APP_PASSWORD`        | Secret/password for the registered bot                                     | ✅       | –       |


---
* `{PROVIDER}_API_KEY`- Replace the *{PROVIDER}* with the  **LLM_MODEL_PROVIDER_NAME** (in Uppercase). For example , OPENAI_API_KEY or GOOGLE_GENAI_API_KEY etc.

## 🧾 Summarization Configuration

| Variable                                  | Description                                                                                   | Required | Default       |
|------------------------------------------|-----------------------------------------------------------------------------------------------|----------|----------------|
| `SUMMARIZATION_LLM_MODEL_PROVIDER_NAME`  | LLM provider to use specifically for summarization (fallbacks to core provider if unset)      | ❌       | Provider above |
| `SUMMARIZATION_LLM_MODEL_NAME`           | LLM model name for summarization (fallbacks to core model if unset)                           | ❌       | Model above    |
| `SUMMARIZATION_LLM_MODEL_KEY`           | LLM model key for summarization (fallbacks to core model if unset)                           | ❌       | above key    |
| `MIN_MSG_TO_RETAIN`                      | Minimum messages to keep before summarizing earlier messages                                  | ✅       | 5              |
| `MIN_MSG_TO_SUMMARIZE`                   | Minimum messages required (beyond retained) to trigger summarization                          | ✅       | 5              |

---

## 🔐 Airflow Authentication

| Variable              | Description                                                                  | Required | Default      |
|----------------------|------------------------------------------------------------------------------|----------|--------------|
| `AIRFLOW_AUTH_STRATEGY` | Defines credential strategy: `centralized` or `per_user`                     | ✅       | `per_user`|

### Centralized Strategy

| Variable               | Description                                      | Required |
|-----------------------|--------------------------------------------------|----------|
| `AIRFLOW_BASE_URL`    | Base URL of your Apache Airflow instance         | ✅       |
| `AIRFLOW_USER_NAME`   | Global user for calling Airflow APIs             | ✅       |
| `AIRFLOW_USER_PASSWORD`| Password for the global Airflow user             | ✅       |

### Per User Strategy

| Variable              | Description                                               | Required |
|----------------------|-----------------------------------------------------------|----------|
| `FERNET_SECRET_KEY`  | Secret key used for encrypting user credentials in the DB | ✅       |




### Variable for Local Deployment

| Variable              | Description                                               | Required |
|----------------------|-----------------------------------------------------------|----------|
| `AZURE_BOT_NAME`        | Name of the Bot that you have created. e.g Airflow-Copilot                                     | ❌       | –       |
| `NGROK_AUTHTOKEN`        |NGROK Auth Token                                     | ✅       | –       |

---


## 🔍 Environment Variable Details

1. **`LLM_MODEL_PROVIDER_NAME`**  
    - **Description**: Name of the LLM provider responsible for AI/agent interactions.  
    - **Default**: _None_  
    - **Possible values**: `openai`, `google_genai`, `anthropic`.  
    - **Required**: ✅ Yes  

2. **`LLM_MODEL_NAME`**  
    - **Description**: The LLM model used for primary reasoning and responses.  
    - **Default**: _None_  
    - **Possible values**: `gpt-4`, `mixtral-8x7b`, `gemini-pro`, etc.  
    - **Required**: ✅ Yes  

3. **`{PROVIDER}_API_KEY`**  
    - **Description**: API key used to authenticate with the selected LLM provider. Replace `{PROVIDER}` with the uppercase value of `LLM_MODEL_PROVIDER_NAME`.  
    - **Default**: _None_  
    - **Possible values**: Varies by provider  
    - **Required**:                                                                      

4. **`DB_URI`**  
        - **Description**: PostgreSQL URI used for persisting state, conversation checkpoints, and user credentials.  
        - **Default**: _None_  
        - **Possible values**: e.g., `'postgresql://username:password@host:port/db'`  
        - **Required**: ✅ Yes  

5. **`MICROSOFT_APP_ID`**  
    - **Description**: Azure Bot registration ID. Required to connect your bot to Microsoft Teams.  
    - **Default**: _None_  
    - **Possible values**: Azure-generated GUID  
    - **Required**: ✅ Yes  

6. **`MICROSOFT_APP_PASSWORD`**  
    - **Description**: Secret associated with the Azure Bot App ID.  
    - **Default**: _None_  
    - **Possible values**: Azure-generated client secret  
    - **Required**: ✅ Yes  

7. **`SUMMARIZATION_LLM_MODEL_PROVIDER_NAME`**  
    - **Description**: Optional override for the LLM provider used in summarization. Falls back to the main provider if not set.  
    - **Default**: value of `LLM_MODEL_PROVIDER_NAME`  
    - **Possible values**: Same as LLM providers  
    - **Required**: ❌ Optional  

8. **`SUMMARIZATION_LLM_MODEL_NAME`**  
    - **Description**: Optional override for the model used in summarization. Falls back to main model if not set.  
    - **Default**: value of `LLM_MODEL_NAME`  
    - **Possible values**: Same as other models  
    - **Required**: ❌ Optional  

9. **`MIN_MSG_TO_RETAIN`**  
    - **Description**: Number of most recent user/tool messages to retain in memory before summarization.  
    - **Default**: `10`  
    - **Possible values**: Integer > 0  
    - **Required**: ✅ Yes  

10. **`MIN_MSG_TO_SUMMARIZE`**  
    - **Description**: Minimum number of messages beyond retained ones to trigger summarization.  
    - **Default**: `10`  
    - **Possible values**: Integer > 0  
    - **Required**: ✅ Yes  

11. **`AIRFLOW_AUTH_STRATEGY`**  
    - **Description**: Defines how Airflow credentials are managed – centrally or per user.  
    - **Default**: `per_user`  
    - **Possible values**: `centralized`, `per_user`  
    - **Required**: ✅ Yes  

12. **`AIRFLOW_BASE_URL`**  
    - **Description**: Base URL of the Airflow instance used for API calls.  
    - **Default**: _None_  
    - **Possible values**: e.g., `https://<host>:<port>`  
    - **Required**: ✅ Yes  

13. **`AIRFLOW_USER_NAME`**  
    - **Description**: Username for Airflow (only for centralized strategy).  
    - **Default**: _None_  
    - **Possible values**: Any valid Airflow user  
    - **Required**: ✅ Yes (if `centralized`)  

14. **`AIRFLOW_USER_PASSWORD`**  
    - **Description**: Password for Airflow user (only for centralized strategy).  
    - **Default**: _None_  
    - **Possible values**: Any valid password  
    - **Required**: ✅ Yes (if `centralized`)  

15. **`FERNET_SECRET_KEY`**  
    - **Description**: Encryption key used to store user-specific Airflow credentials in the database.  
    - **Default**: _None_  
    - **Possible values**: Base64-encoded 32-byte key  
    - **Required**: ✅ Yes (if `per_user`) 
    - **Command**: Run below command to generate the key.
    
    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ``` 
    > *Do not change the Farnet key in every deployment otherwise the backend credentials will not be decrypt and every user have to update their cred again.*

16. **`AZURE_BOT_NAME`**
    - **Description**: The Azure Bot Name to automatically update the endpoint while Local Deployment.  
    - **Default**: Airflow-Copilot 
    - **Required**: ❌ Optional 

17. **`NGROK_AUTHTOKEN`**
    - **Description**: The Ngrok Token to deploy the Local Fast API to public Https endpoint.  
    - **Required**: ✅ Yes (for Local deployment) 
