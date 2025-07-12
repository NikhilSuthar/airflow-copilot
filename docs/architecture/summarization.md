# 🧠 Summarization Logic

Airflow Copilot uses a **background summarization mechanism** to intelligently compress long chat histories into concise summaries. This ensures the **LLM’s context window remains optimized** while still preserving essential historical intent and behavior.

---

## 🔍 Why Summarization Is Needed

Modern LLMs have strict token limits, and exceeding those limits leads to:

- ❌ Truncated prompts  
- ⚠️ Incomplete or lost context  
- 🧠 Reduced memory of earlier user requests and responses 
- 💰 More messages = higher cost — especially with large or chatty conversations

To mitigate this, Airflow Copilot **trims older messages** into concise summaries after a certain threshold — **while preserving the most recent interactions verbatim.**

---

## 🧭 How Summarization Works

Each time the message count exceeds a configured threshold, the earliest interactions are summarized and replaced with a compact summary entry.

![Summarization Flow](../assets/Summarization.svg){ .center-img }

*Summarization replaces verbose chat history with a condensed version while keeping the latest messages intact.*

---

# 🛡️ Design Notes

✅ Messages are not deleted from the database — only trimmed from in-memory state.  
✨ Summaries are maintained in a separate key: `state["summary"]`.  
🔁 Summarization is triggered automatically when the total message count exceeds  
`MIN_MSG_TO_SUMMARIZE + MIN_MSG_TO_RETAIN`.  
🔍 Last human message before the cutoff is preserved, ensuring summarization doesn't split active interactions or commands. 

---

## 🧪 Tuning Parameters

Control summarization behavior through the following environment variables:

| Variable                | Description                                              | Default |
|------------------------|----------------------------------------------------------|---------|
| `MIN_MSG_TO_SUMMARIZE` | Minimum messages required before summarization kicks in  | `10`    |
| `MIN_MSG_TO_RETAIN`    | Number of recent messages to retain without summarizing  | `10`    |

> 💡 This only affects runtime memory. To fully delete stored messages, see the **Delete History** section.  
> ⚠️ Avoid setting the values too low — this may lead to excessive summarization and increased LLM usage.  
> ✅ Recommended: use a lightweight or cost-effective model for summarization.

---

## 🧠 Benefits

- ✅ Keeps LLM context window small and efficient  
- 🧠 Preserves conversation continuity in compressed form  
- 🚫 Prevents token overflow for long or technical sessions  
- 🔄 Enables smooth, reliable, long-running conversations  

---

## 💬 Example: Airflow DAG Interaction

Let’s walk through a typical conversation and how it might be summarized:

### 🗨️ Full Interaction Before Summarization

**Prior Summary:** None  

**Human:**  
Hello

**AI:**  
Calling greet tool...

**Tool Call:**  
`greet(user_name='John')`

**AI:**  
Hello John, how can I assist you with Airflow?

**Human:**  
Can you show me the latest DAG runs for `load_sales_data`?

**AI:**  
`call get_dag_runs tool with dag id 'load_sales_data'`

**Tool Call:**  
`get_dag_runs(dag_id='load_sales_data')`

**AI:**  
Here are the last 3 DAG runs:  
- `run_2024_06_01` – ✅ Success  
- `run_2024_06_02` – ❌ Failed  
- `run_2024_06_03` – ✅ Success

**Human:**  
Please retry the failed run.

**AI:**  
Retrying `run_2024_06_02` for DAG `load_sales_data`.

**Tool Call:**  
`trigger_dag(dag_id='load_sales_data', dag_run_id='run_2024_06_02')`

**AI:**  
The failed DAG has been triggered.

---

### 🧾 After Summarization

**Summarization:**  
The user, John, initiated a greeting and requested the latest DAG runs for `load_sales_data`. The assistant retrieved three recent runs, identifying `run_2024_06_02` as failed. Upon user request, that run was successfully re-triggered through the API.

---

### 🗨️ Interaction After Summarization

**Prior Summary:**  
The user, John, initiated a greeting and requested the latest DAG runs for `load_sales_data`. The assistant retrieved three recent runs, identifying `run_2024_06_02` as failed. Upon user request, that run was successfully re-triggered through the API.

**Human:**  
Can you tell me if the DAG ran successfully?

**AI:**  
Yes, the DAG `load_sales_data` has run successfully. The current status is `Success`, and the run ID is `run_2024_06_02`.

---

>💡 In the above conversation, the copilot did not ask for `dag_id` or `dag_run_id` again — it inferred those from the summary context.

>Without summarization, the next LLM call would include all 13 messages (12 from previous interactions + 1 new user message).

>With summarization, the same context is preserved using just 2 messages:
the summary and the new user message — resulting in a significant token and cost reduction.

## 📌 Final Note

Summarization is completely transparent to the user. It’s designed to:

- ✅ Optimize performance  
- 🧠 Prevent model context loss  
- 🔁 Maintain long conversation continuity  

Even across hundreds of exchanges, **Airflow Copilot** remains context-aware, memory-efficient, and responsive.


## 🔗 Next Steps

- **[Refresh History](/architecture/refresh_history)**: How to delete/purge user conversation with Airflow copilot from backend database(postgres)
- **[Supported Airflow Copilot Features](/architecture/supported_apis)**: List of activity Airflow copilot can do.
- **[Airflow Auth Type](/architecture/airflow_auth_type)**: Airflow Auth type supported to authentication.
- **[Environment Variables](/configuration/environment_variables)**: Configration details of Airflow Copilot.

