
# 🏋️ Supported Capabilities
**Airflow Copilot** is designed to assist with **informational and on-demand operations** in Apache Airflow. It enables users to query metadata, trigger DAGs, inspect task details, and more — all without directly accessing the Airflow UI.

> **Security-first Design**:
> *Airflow Copilot does not support deletion of DAGs to avoid accidental or unauthorized changes. Instead, it allows you to **disable (pause)** a DAG to prevent it from running.*

------

> **DAG Trigger Convention:**  
> *Any DAG run initiated by Copilot uses a `genai_` prefix in the `dag_run_id`, making it easy to identify which runs were triggered by the assistant.*

The following sections provide a categorized summary of what you can do with Airflow Copilot via **Microsoft Teams** or API integration.

## DAGs

-    Get all dags
-  Get dag information
-  Get dag details
-  Enable dag
-  Disable dag
-  Trigger dag
-  Get dag runs
-  Get specific dag run
-  Update dag state
-  Update dag run note
-  Get dag source code
-  Get dag run
-  List all dag runs
-  Get dag warning

## Tasks

-  Get tasks
-  Get task details
-  Get task instances
-  List task instances in dag run
-  Get task instance
-  Update task instances
-  Get task log url

## Variables

-  List variables
-  Get variable
-  Set variable

## Connections

-  List connections
-  Get connection
-  Update connection

## Pools

-  List pools
-  Get pool
-  Create pool
-  Update pool

## Roles and Permissions

-  List permissions
-  List roles
-  Get role
-  Create role
-  Update role

## Users

-  List users
-  Get user
-  Create user
-  Update user

## XComs

-  List xcoms for task
-  Get xcom

## Logs

-  List event logs
-  Get event logs
-  Get task log url

## System Info

-  Get info
-  Get config
-  Get health
-  Get version

## Plugins & Providers

-  List plugins
-  List providers

## Import Errors

-  List import error
-  Get import error

## Datasets

-  List datasets
-  List dataset triggered dags


## 🔗 Next Steps


- **[Agent Behavior Notes & Known Limitations](../../quickstart/agent-behavior)**: Some know Airflow Copilot behaviour and Limitations.


## 🔗 Next Steps

- **[Refresh History](../refresh_history)**: How to delete/purge user conversation with Airflow copilot from backend database(postgres)
- **[Airflow Auth Type](../airflow_auth_type)**: Airflow Auth type supported to authentication.
- **[Environment Variables](../../configuration/environment_variables)**: Configration details of Airflow Copilot.