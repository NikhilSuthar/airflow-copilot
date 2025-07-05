# airflow_teams_bot/tools.py

from langchain_core.tools import tool
import httpx
import datetime
from functools import lru_cache
from airflow_copilot.config.settings import get_environment
import secrets,string
from airflow_copilot.config.CredentialStore import get_user_credentials
from airflow_copilot.config.settings import user_id_context
import logging as logs




class AirflowTools:
    _env = get_environment()

    @classmethod
    async def _make_request(cls, args:dict):
        if cls._env.auth_strategy == "centralized":
            logs.info(f"Fetching Airflow Credential from Environment.")
            username = cls._env.airflow_user_name
            password = cls._env.airflow_user_pass
        else:
            try:
                logs.info(f"Fetching Airflow Credential from Database.")
                user_id = user_id_context.get()
                
            except LookupError:
                raise ValueError("User id context variable not set, issue occur while fetching airflow credential.")
            (username,password) = await get_user_credentials(thread_id=user_id)
            logs.info(f"Airflow Credential fetch from Database for user id {user_id}.")

        if username is None or password is None:
            return f"Credential not found, Please Update credeital using Prompt **Update my Airflow Credential** "
        else:
            url = args["url"]
            method = args["method"]
            payload = args["payload"]
            try:
                async with httpx.AsyncClient() as client:
                    if method.upper() == "GET":
                        response = await client.get(url, auth=(username, password))
                    elif method.upper() == "POST":
                        response = await client.post(url, auth=(username, password), json=payload)
                    elif method.upper() == "PATCH":
                        response = await client.patch(url, auth=(username, password), json=payload)
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")
                    return response.text
            except Exception as e:
                return f"❌ Error: {str(e)}"
       
    @staticmethod
    @tool
    async def greet(user_name: str) -> str:
        """Greet the user by name.
        Args:
            user_name: The name of the user to greet.
        Returns:
            A greeting string including the user's name."""
        return f"Hello, {user_name}!"

    @staticmethod
    @tool
    async def get_all_dags() -> str:
        """Retrieve the list of all DAGs registered in Airflow.
        Returns:
            The JSON response as a string containing metadata of all DAGs."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_dag_details(dag_id: str) -> str:
        """Retrieve extended details of a specific DAG.
        Args:
            dag_id: The ID of the DAG to retrieve.
        Returns:
            Extended metadata and configuration of the DAG."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/details", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_dag_information(dag_id: str) -> str:
        """Retrieve basic metadata of a specific DAG (e.g., is_paused, schedule).
        Args:
            dag_id: The ID of the DAG.
        Returns:
            Basic information about the DAG."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_dag_runs(dag_id: str) -> str:
        """Get all DAG run records for a specific DAG.
        Args:
            dag_id: The ID of the DAG.
        Returns:
            A list of DAG run metadata (status, execution date, etc.)."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_specific_dag_run(dag_id: str, dag_run_id: str) -> str:
        """Get details of a specific DAG run.
        Args:
            dag_id: The ID of the DAG.
            dag_run_id: The ID of the specific DAG run.
        Returns:
            Metadata and status of the specified DAG run."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    
    @staticmethod
    @tool
    async def get_task_instances(dag_id: str) -> str:
        """List all task instances for a specific DAG.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response with task instance details."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/taskInstances", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_task_instances(dag_id: str, dag_run_id: str, execution_date: str, state: str, task_id: str) -> str:
        """Update state of multiple task instances in a DAG run.
        Args:
            dag_id: The DAG ID.
            dag_run_id: The DAG run ID.
            execution_date: The execution date of the DAG run.
            state: New state to apply (e.g., 'success', 'failed').
            task_id: Task ID to update.
        Returns:
            JSON response confirming update action."""
        payload = {
            "dag_run_id": dag_run_id,
            "dry_run": "true",
            "execution_date": execution_date,
            "include_downstream": "true",
            "include_future": "true",
            "include_past": "true",
            "include_upstream": "true",
            "new_state": state,
            "task_id": task_id
        }
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/taskInstances", "method": "GET", "payload": payload}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_dag_state(dag_id: str, dag_run_id: str, new_state: str) -> str:
        """Update the state of a DAG run.
        Args:
            dag_id: The DAG ID.
            dag_run_id: The DAG run ID.
            new_state: Target state ('success' or 'failed').
        Returns:
            JSON response indicating success or failure."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}", "method": "PATCH", "payload": {"state": new_state}}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_dag_run_note(dag_id: str, dag_run_id: str, note: str) -> str:
        """Update the note attached to a DAG run (Airflow ≥ 2.5.0).
        Args:
            dag_id: The DAG ID.
            dag_run_id: The DAG run ID.
            note: The note to attach to the run.
        Returns:
            JSON response after note update."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/setNote", "method": "PATCH", "payload": {"note": note}}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_event_logs() -> str:
        """List all event logs in Airflow.
        Returns:
            JSON response with event log entries."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/eventLogs", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_event_logs(event_log_id: str) -> str:
        """Get details of a specific event log entry.
        Args:
            event_log_id: The ID of the event log.
        Returns:
            JSON response with log details."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/eventLogs/{event_log_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_providers() -> str:
        """List all installed Airflow providers.
        Returns:
            JSON response with provider metadata."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/providers", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_plugins() -> str:
        """List all available Airflow plugins.
        Returns:
            JSON response with plugin details."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/plugins", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_import_error() -> str:
        """List all DAG import errors in Airflow.
        Returns:
            JSON response with import error info."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/importErrors", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_import_error(import_error_id: str) -> str:
        """Get details of a specific import error.
        Args:
            import_error_id: ID of the import error entry.
        Returns:
            JSON response with error information."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/importErrors/{import_error_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_pools() -> str:
        """List all Airflow pools.
        Returns:
            JSON response with all pools and their properties."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/pools", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_pool(pool_name: str) -> str:
        """Get details of a specific Airflow pool.
        Args:
            pool_name: Name of the pool to fetch.
        Returns:
            JSON response with the pool's metadata."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_pool(pool_name: str, slot_count: int, description: str = "") -> str:
        """Update an existing Airflow pool.
        Args:
            pool_name: Name of the pool to update.
            slot_count: Number of slots in the pool.
            description: Optional description of the pool.
        Returns:
            JSON response after updating the pool."""
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}",
            "method": "PATCH",
            "payload": {
                "name": pool_name,
                "slots": slot_count,
                "description": description
            }
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def create_pool(pool_name: str, slot_count: int, description: str = "") -> str:
        """Create a new Airflow pool or overwrite if it exists.
        Args:
            pool_name: Name of the pool.
            slot_count: Number of slots (must be ≥ 0).
            description: Optional description for the pool.
        Returns:
            JSON response after creating the pool."""
        if slot_count < 0:
            raise ValueError("slot_count must be >= 0")
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}",
            "method": "POST",
            "payload": {
                "name": pool_name,
                "slots": slot_count,
                "description": description
            }
        }
        return await AirflowTools._make_request(args=args)

    
    @staticmethod
    @tool
    async def list_permissions() -> str:
        """List all available permissions in Airflow.
        Returns:
            JSON response with action-resource pairs."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/permissions", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_roles() -> str:
        """List all roles configured in Airflow.
        Returns:
            JSON response with all role definitions."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/roles", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_role(role_name: str) -> str:
        """Get details for a specific role.
        Args:
            role_name: The name of the role.
        Returns:
            JSON response with role permissions and metadata."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/roles/{role_name}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def create_role(role_name: str, permissions: list[dict] = []) -> str:
        """Create a new role with action-resource permissions.
        Args:
            role_name: The name of the new role.
            permissions: List of {'action': str, 'resource': str} mappings.
        Returns:
            JSON response confirming role creation."""
        default_permission = {"action": "can_read", "resource": "Website"}
        full_permissions = permissions + [default_permission]
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/roles",
            "method": "POST",
            "payload": {
                "name": role_name,
                "actions": [
                    {
                        "action": {"name": p["action"]},
                        "resource": {"name": p["resource"]}
                    } for p in full_permissions
                ]
            }
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_role(role_name: str, action: str, resource: str) -> str:
        """Update a role by adding or modifying a permission.
        Args:
            role_name: The name of the role.
            action: The action to assign (e.g., 'can_read').
            resource: The resource (e.g., 'DAG:sales_dag').
        Returns:
            JSON response after role update."""
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/roles/{role_name}",
            "method": "PATCH",
            "payload": {
                "name": role_name,
                "actions": [
                    {
                        "action": {"name": action},
                        "resource": {"name": resource}
                    }
                ]
            }
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_tasks(dag_id: str) -> str:
        """List all tasks in a given DAG.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response with all task metadata in the DAG."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/tasks", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_task_details(dag_id: str, task_id: str) -> str:
        """Get metadata of a specific task in a DAG.
        Args:
            dag_id: The DAG identifier.
            task_id: The task identifier.
        Returns:
            JSON response with task details."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/tasks/{task_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_dag_run(dag_id: str) -> str:
        """List all DAG runs for a given DAG.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response with all run instances."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def trigger_dag(dag_id: str) -> str:
        """Trigger a new DAG run manually.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response with triggered run metadata."""
        dag_run_id = f"genai_trigger__{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "POST", "payload": {"dag_run_id": dag_run_id}}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def disable_dag(dag_id: str) -> str:
        """Pause a DAG to disable its scheduling.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response confirming the update."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "PATCH", "payload": {"is_paused": True}}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def enable_dag(dag_id: str) -> str:
        """Unpause a DAG to enable its scheduling.
        Args:
            dag_id: The DAG identifier.
        Returns:
            JSON response confirming the update."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "PATCH", "payload": {"is_paused": False}}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_all_dag_runs() -> str:
        """List all DAG runs across all DAGs.
        Returns:
            JSON response with all DAG run metadata."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dagRuns", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_task_instances_in_dag_run(dag_id: str, dag_run_id: str) -> str:
        """List all task instances in a DAG run.
        Args:
            dag_id: The DAG identifier.
            dag_run_id: The DAG run identifier.
        Returns:
            JSON response with task instance data."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_task_instance(dag_id: str, dag_run_id: str, task_id: str) -> str:
        """Get details for a specific task instance in a DAG run.
        Args:
            dag_id: The DAG identifier.
            dag_run_id: The DAG run ID.
            task_id: The task ID.
        Returns:
            JSON response with task instance details."""
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)
    
    @staticmethod
    @tool
    async def get_health() -> str:
        """Check Airflow health status.
        Returns:
            JSON health check result from Airflow's REST API.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/health", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_version() -> str:
        """Get Airflow version.
        Returns:
            JSON containing Airflow version.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/version", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_config() -> str:
        """Fetch Airflow configuration.
        Returns:
            JSON with Airflow configuration sections and values.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/config", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_info() -> str:
        """Fetch general metadata about the Airflow instance.
        Returns:
            JSON with metadata including version, executor, and more.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/info", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_variables() -> str:
        """List all Airflow variables.
        Returns:
            JSON with all configured Airflow variables.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/variables", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_variable(var_key: str) -> str:
        """Get the value of a specific Airflow variable.
        Args:
            var_key: Key of the variable.
        Returns:
            JSON with variable key and value.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/variables/{var_key}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def set_variable(var_key: str, value: str) -> str:
        """Set or update an Airflow variable.
        Args:
            var_key: Variable key to set.
            value: Value to assign.
        Returns:
            JSON confirmation of variable update.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/variables/{var_key}",
            "method": "PATCH",
            "payload": {"key": var_key, "value": value}
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_connections() -> str:
        """List all Airflow connections.
        Returns:
            JSON with all configured connections.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/connections", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_connection(connection_id: str) -> str:
        """Get details of a specific Airflow connection.
        Args:
            connection_id: ID of the connection.
        Returns:
            JSON with connection info.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/connections/{connection_id}",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_connection(connection_id: str, body: dict) -> str:
        """Update a specific Airflow connection.
        Args:
            connection_id: ID of the connection to update.
            body: Dictionary containing updated fields.
        Returns:
            JSON confirmation of update.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/connections/{connection_id}",
            "method": "PATCH",
            "payload": body
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_datasets() -> str:
        """List all datasets.
        Returns:
            JSON with all datasets and their metadata.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/datasets", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_dataset_triggered_dags(dataset_id: str) -> str:
        """List DAGs triggered by a given dataset.
        Args:
            dataset_id: ID of the dataset.
        Returns:
            JSON with DAGs consuming this dataset.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/datasets/{dataset_id}/consuming_dags",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_dag_source_code(file_token: str) -> str:
        """Fetch DAG source code by file token.
        Args:
            file_token: Token of the file obtained from DAG details.
        Returns:
            Raw DAG source code.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/dagSources/{file_token}", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_xcoms_for_task(dag_id: str, dag_run_id: str, task_id: str) -> str:
        """List all XCom entries for a specific task instance.
        Args:
            dag_id: DAG ID.
            dag_run_id: DAG run ID.
            task_id: Task ID.
        Returns:
            JSON list of XCom entries.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def list_users() -> str:
        """List all users in Airflow.
        Returns:
            JSON list of user records.
        """
        args = {"url": f"{AirflowTools._env.airflow_base_url}/users", "method": "GET", "payload": None}
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_user(username: str) -> str:
        """Get details for a specific Airflow user.
        Args:
            username: Username of the user.
        Returns:
            JSON with user details.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/users/{username}",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def update_user(username: str, role_name: str, password: str, email: str = "", first_name: str = "", last_name: str = "") -> str:
        """Update user details in Airflow.
        Args:
            username: Username of the user.
            role_name: Role to assign.
            password: User's password.
            email: Optional email address.
            first_name: Optional first name.
            last_name: Optional last name.
        Returns:
            JSON confirmation of user update.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/users/{username}",
            "method": "PATCH",
            "payload": {
                "username": username,
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "roles": [{"name": role_name}]
            }
        }
        return await AirflowTools._make_request(args=args)
    
    @staticmethod
    @tool
    async def get_dag_warning() -> str:
        """Check for any DAG warnings in Airflow.
        Returns:
            A JSON string containing warnings related to DAGs.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/dagWarnings/",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def create_user(
        username: str,
        role_name: str,
        email: str = "",
        password: str = "",
        first_name: str = "",
        last_name: str = ""
    ) -> str:
        """Create a new Airflow user and assign a role.
        If no password is provided, a strong random password is generated.

        Args:
            username: Username of the new user.
            role_name: Role to assign (e.g., 'Admin', 'User').
            email: User's email address.
            password: Optional password. If empty, a secure password is generated.
            first_name: Optional first name.
            last_name: Optional last name.

        Returns:
            JSON response of the user creation request.
        """
        if str(password).strip() == "":
            valid_symbols = "!@#%^*()-+"
            valid_letters = ''.join(c for c in string.ascii_letters if c not in "lI1O0")
            valid_digits = '23456789'
            characters = valid_letters + valid_digits + valid_symbols
            password = ''.join(secrets.choice(characters) for _ in range(12))

        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/users",
            "method": "POST",
            "payload": {
                "username": username,
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "roles": [{"name": role_name}]
            }
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_xcom(dag_id: str, dag_run_id: str, task_id: str, xcom_key: str) -> str:
        """Fetch a specific XCom value from a task instance.
        
        Args:
            dag_id: DAG ID.
            dag_run_id: DAG run ID.
            task_id: Task ID.
            xcom_key: XCom key to retrieve.

        Returns:
            JSON string with the XCom value.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def get_task_log_url(dag_id: str, dag_run_id: str, task_id: str, try_number: int = 1) -> str:
        """Fetch the log output of a specific task instance.
        
        Args:
            dag_id: DAG ID.
            dag_run_id: DAG run ID.
            task_id: Task ID.
            try_number: The task execution attempt number (default is 1).

        Returns:
            JSON string containing log URL or log content.
        """
        args = {
            "url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}",
            "method": "GET",
            "payload": None
        }
        return await AirflowTools._make_request(args=args)

    @staticmethod
    @tool
    async def otherwise() -> str:
        """Fallback tool for unsupported queries or invalid requests.
        
        Returns:
            A predefined fallback message.
        """
        return "I will not be able to provide output for your input..."

    
       
    @classmethod
    def get_all_tools(cls):
        return [
            cls.greet,
            cls.otherwise,
            cls.get_info,
            cls.get_config,
            cls.get_health,
            cls.get_version,
            cls.get_all_dags,
            cls.get_dag_information,
            cls.get_dag_details,
            cls.get_dag_warning,
            cls.get_dag_source_code,
            cls.enable_dag,
            cls.disable_dag,
            cls.trigger_dag,
            cls.list_all_dag_runs,
            cls.get_dag_run,
            cls.get_dag_runs,
            cls.get_specific_dag_run,
            cls.update_dag_state,
            cls.update_dag_run_note,
            cls.get_tasks,
            cls.get_task_details,
            cls.get_task_instances,
            cls.list_task_instances_in_dag_run,
            cls.get_task_instance,
            cls.update_task_instances,
            cls.get_task_log_url,
            cls.list_xcoms_for_task,
            cls.get_xcom,
            cls.list_variables,
            cls.get_variable,
            cls.set_variable,
            cls.list_connections,
            cls.get_connection,
            cls.update_connection,
            cls.list_pools,
            cls.get_pool,
            cls.create_pool,
            cls.update_pool,
            cls.list_permissions,
            cls.list_roles,
            cls.get_role,
            cls.create_role,
            cls.update_role,
            cls.list_users,
            cls.get_user,
            cls.create_user,
            cls.update_user,
            cls.list_event_logs,
            cls.get_event_logs,
            cls.list_plugins,
            cls.list_providers,
            cls.list_import_error,
            cls.get_import_error,
            cls.list_datasets,
            cls.list_dataset_triggered_dags
        ]
