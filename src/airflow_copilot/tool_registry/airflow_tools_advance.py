# airflow_teams_bot/tools.py

from langchain_core.tools import tool
import httpx
import datetime
from functools import lru_cache
from airflow_copilot.config.settings import get_environment
import secrets,string


class AirflowTools:
    _env = get_environment()
    
    @staticmethod
    @tool
    def greet(user_name: str) -> dict:
        """Greet the user by name.""" 
        return {"url": None, "method": None, "payload": None, "message":  f"Hello, {user_name}!"}
    
    @staticmethod
    @tool
    def get_all_dags() -> dict:
        """Get URL to list all DAGs."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags", "method": "GET", "payload": None}
    
    @staticmethod
    @tool
    def get_dag_details(dag_id: str, ) -> dict:
        """Get URL for exteded details of a specific DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/details", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_dag_information(dag_id: str, ) -> dict:
        """Get URL for basic information of a specific DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_dag_runs(dag_id: str) -> dict:
        """Get URL to list all runs for a specific DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_specific_dag_run(dag_id: str, dag_run_id: str) -> dict:
        """Get URL for a specific DAG run."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_task_instances(dag_id: str) -> dict:
        """Get URL to list all task instances for a DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/taskInstances", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def update_task_instances(dag_id: str,dag_run_id: str, execution_date: str, state: str, task_id: str ) -> dict:
        """Get URL to Updates the state for multiple task instances simultaneously."""
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
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/taskInstances", "method": "GET", "payload": payload}

    @staticmethod
    @tool
    def update_dag_state(dag_id: str, dag_run_id: str, new_state: str)-> dict:
        """
            Get URL to modify the DAG run state.

            Parameters:
            - dag_id: DAG identifier
            - dag_run_id: DAG run identifier
            - new_state: Desired state for the task instance

            new_state allowed values:
            - 'success'
            - 'failed'

            Returns:
                Dictionary with API call details.
            """
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}",
            "method":"PATCH",
            "payload": {"state": new_state}
        }

    @staticmethod
    @tool
    def update_dag_run_note(dag_id: str, dag_run_id: str, note: str) -> dict:
        """Update the Note of Dag run id, only applicable verion above 2.5.0"""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/setNote",
            "method":"PATCH",
            "payload": {"note": note}
        }
    
    @staticmethod
    @tool
    def list_event_logs() -> dict:
        """Get URL to List log entries from event log."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/eventLogs",
            "method":"GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def get_event_logs(event_log_id: str) -> dict:
        """Get URL to get log id details."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/eventLogs/{event_log_id}",
            "method":"GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def list_providers() -> dict:
        """Get URL to list all airflow providers."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/providers",
            "method":"GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def list_plugins() -> dict:
        """Get URL to list all airflow plugins."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/plugins",
            "method":"GET",
            "payload": None
        }

    @staticmethod
    @tool
    def list_import_error() -> dict:
        """Get URL to List all import error DAG."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/importErrors",
            "method":"GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def get_import_error(import_error_id: str) -> dict:
        """Get URL to get details of specific import error id."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/importErrors/{import_error_id}",
            "method":"GET",
            "payload": None
        }

    @staticmethod
    @tool
    def list_pools() -> dict:
        """
        List all Airflow pools.

        Returns:
            A GET request to fetch all pools with their details.
        """
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/pools",
            "method": "GET",
            "payload": None
        }


    @staticmethod
    @tool
    def get_pool(pool_name: str) -> dict:
        """
        Get details of a specific Airflow pool.

        Parameters:
        - pool_name: Name of the pool to fetch.

        Returns:
            A GET request for the specific pool.
        """
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def update_pool(pool_name: str, slot_count: int, description: str = "") -> dict:
        """
        Create or update an Airflow pool.

        Parameters:
        - pool_name: Name of the pool to create or update.
        - slot_count: Number of slots for the pool.
        - description: Optional description.

        Returns:
            A PATCH request to update the pool.
        """
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}",
            "method": "PATCH",
            "payload": {
                "name": pool_name,
                "slots": slot_count,
                "description": description
            }
        }


    @staticmethod
    @tool
    def create_pool(pool_name: str, slot_count: int, description: str = "") -> dict:
        """
        Create a new Airflow pool. If the pool already exists, it will be overwritten.

        Parameters:
        - pool_name: Name of the pool to create.
        - slot_count: Number of slots in the pool. Must be a non-negative integer.
        - description: Optional description for the pool.

        Returns:
            A POST request to create the pool.
        """
        if slot_count < 0:
            raise ValueError("slot_count must be >= 0")

        return {
            "url": f"{AirflowTools._env.airflow_base_url}/pools/{pool_name}",
            "method": "POST",
            "payload": {
                "name": pool_name,
                "slots": slot_count,
                "description": description
            }
        }

    @staticmethod
    @tool
    def list_permissions() -> dict:
        """Get URL to List all permissions."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/permissions",
            "method":"GET",
            "payload": None
        }

    @staticmethod
    @tool
    def list_roles() -> dict:
        """Get URL to List all roles."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/roles",
            "method":"GET",
            "payload": None
        }

    @staticmethod
    @tool
    def get_role(role_name: str) -> dict:
        """Get URL to get user role."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/roles/{role_name}",
            "method":"GET",
            "payload": None
        }

    @staticmethod
    @tool
    def create_role(role_name: str, permissions: list[dict] = []) -> dict:
        """
        Create a custom role with multiple action-resource pairs.
        Automatically adds `can_read` on Website as default.

        permissions format:
        [
            {"action": "can_read", "resource": "DAG:{dag_id}"},
        ]

        Possible action values:
        - can_read
        - can_edit
        - can_delete
        - can_create
        """

        # Ensure "can_read" on Website is always included
        default_permission = {"action": "can_read", "resource": "Website"}
        full_permissions = permissions + [default_permission]

        return {
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

    @staticmethod
    @tool
    def update_role(role_name:str, action:str, resource: str) -> dict:
        """Get URL to Update the role."""
        return {
            "url":f"{AirflowTools._env.airflow_base_url}/roles/{role_name}",
            "method":"PATCH",
            "payload": {
                    "actions": [
                        {
                        "action": {
                            "name": action
                        },
                        "resource": {
                            "name": resource
                        }
                        }
                    ],
                    "name": role_name
                    }
        }

    @staticmethod
    @tool
    def get_tasks(dag_id: str, ) -> dict:
        """Get URL to list all tasks for a DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/tasks", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_task_details(dag_id: str, task_id: str, ) -> dict:
        """Get URL for details of a specific task in a DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/tasks/{task_id}", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_dag_run(dag_id: str, ) -> dict:
        """Get URL for DAG run."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def trigger_dag(dag_id: str, ) -> dict:
        """Get URL to trigger DAG."""
        dag_run_id = f"genai_trigger__{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns", "method": "POST", "payload": {"dag_run_id": dag_run_id}}

    @staticmethod
    @tool
    def disable_dag(dag_id: str, ) -> dict:
        """Get URL to disable a DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "PATCH", "payload": {"is_paused": True}}

    @staticmethod
    @tool
    def enable_dag(dag_id: str, ) -> dict:
        """Get URL to enable a DAG."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}", "method": "PATCH", "payload": {"is_paused": False}}

    @staticmethod
    @tool
    def list_all_dag_runs() -> dict:
        """Get URL to list all DAG runs."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dagRuns", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def list_task_instances_in_dag_run(dag_id: str, dag_run_id: str, ) -> dict:
        """Get URL to list all task instances in a specific DAG run."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_task_instance(dag_id: str, dag_run_id: str, task_id: str, ) -> dict:
        """Get URL for a specific task instance in a DAG run."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_health() -> dict:
        """Get URL to check Airflow health."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/health", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_version() -> dict:
        """Get URL to fetch Airflow version."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/version", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_config() -> dict:
        """Get URL to fetch Airflow configuration."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/config", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def get_info() -> dict:
        """Get URL to fetch Airflow metadata."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/info", "method": "GET", "payload": None}

    @staticmethod
    @tool
    def list_variables() -> dict:
        """Get URL to list Airflow variables."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/variables", "method": "GET", "payload": None}
    
    @staticmethod
    @tool
    def get_variable(var_key: str) -> dict:
        """Get a specific Airflow variable."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/variables/{var_key}",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def set_variable(var_key: str, value: str) -> dict:
        """Get URL to Set or update an Airflow variable."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/variables/{var_key}",
            "method": "PATCH",
            "payload": {"key": var_key, "value":value}
        }

    @staticmethod
    @tool
    def list_connections() -> dict:
        """Get URL to list Airflow connections."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/connections", "method": "GET", "payload": None}
    
    @staticmethod
    @tool
    def get_connection(connection_id: str) -> dict:
        """Get a specific Airflow connection."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/connections/{connection_id}",
            "method": "GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def update_connection(connection_id: str, body: dict) -> dict:
        """Get a specific Airflow connection."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/connections/{connection_id}",
            "method": "PATCH",
            "payload": body
        }
    
    # @staticmethod
    # @tool
    # def connection_test(connection_id: str, connection_type: str, host: str, login: str, port: int, schema: str, extra: dict, password: str) -> dict:
    #     """Get a specific Airflow connection."""
    #     return {
    #         "url": f"{AirflowTools._env.airflow_base_url}/connections/test",
    #         "method": "POST",
    #         "payload": {
    #                 "conn_type": connection_type,
    #                 "connection_id": connection_id,
    #                 "description": f"Connection {connection_id} with type {connection_type}",
    #                 "host": host,
    #                 "login": "airflow",
    #                 "port": port,
    #                 "schema": schema,
    #                 "extra": extra,
    #                 "password": password
    #                 }
    #     }
    @staticmethod
    @tool
    def list_datasets() -> dict:
        """List all datasets in Airflow."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/datasets",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def list_dataset_triggered_dags(dataset_id: str) -> dict:
        """List DAGs triggered by a dataset."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/datasets/{dataset_id}/consuming_dags",
            "method": "GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def get_dag_source_code(file_token: str) -> dict:
        """Get the Source code using dag_id's file token, get the file_token from dag_id details"""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dagSources/{file_token}", "method": "GET", "payload": None}
        
    @staticmethod
    @tool
    def list_xcoms_for_task(dag_id: str, dag_run_id: str, task_id: str) -> dict:
        """List all XCom entries for a specific task in a DAG run."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries",
            "method": "GET",
            "payload": None
        }
    
    @staticmethod
    @tool
    def list_users() -> dict:
        """Get URL to list airflow users"""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/users",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def get_user(username: str) -> dict:
        """Get URL to get user details"""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/users/{username}",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def update_user(username: str, role_name: str, password: str, email: str = "", first_name: str = "", last_name: str = "") -> dict:
        """
        Get URL to update Airflow user .

        Parameters:
        - username: Username of the new user
        - role_name: (optional) Role to assign (e.g., 'Admin', 'User', etc.)
        - password: (optional) Password for the user
        - email: (optional) Email address
        - first_name: (optional) First name
        - last_name: (optional) Last name

        Returns:
            Dictionary with Airflow REST API request for user creation.
        """
        return {
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

    @staticmethod
    @tool
    def get_dag_warning() -> dict:
        """Get URL to check dag warning"""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/dagWarnings/",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def create_user(username: str, role_name: str, email: str = "", password: str = "", first_name: str = "", last_name: str = "") -> dict:
        """
        Get URL to create a new Airflow user and assign a role.

        Parameters:
        - username: Username of the new user
        - role_name: Role to assign (e.g., 'Admin', 'User', etc.)
        - email:  Email address
        - password:(optional) Password for the user
        - first_name: (optional) First name or username
        - last_name: (optional) Last name

        Returns:
            Only URL with execution
        """
        if str(password).strip() == "":
            valid_symbols = "!@#%^*()-+"
            valid_letters = ''.join(c for c in string.ascii_letters if c not in "lI1O0")
            valid_digits = '23456789'
            characters = valid_letters + valid_digits + valid_symbols
            # Generate password
            password = ''.join(secrets.choice(characters) for _ in range(12))
        
        return {
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


    @staticmethod
    @tool
    def get_xcom(dag_id: str, dag_run_id: str, task_id: str, xcom_key: str) -> dict:
        """Get a specific XCom value."""
        return {
            "url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}",
            "method": "GET",
            "payload": None
        }

    @staticmethod
    @tool
    def get_task_log_url(dag_id: str, dag_run_id: str, task_id: str, try_number: int = 1, ) -> dict:
        """Get URL to fetch logs for a specific task instance."""
        return {"url": f"{AirflowTools._env.airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}", "method": "GET", "payload": None}
    
    @staticmethod
    @tool
    def otherwise() -> dict:
        """Fallback tool for invalid or unsupported operations."""
        return {"url": None, "method": None, "payload": None, "message": "I will not be able to provide output of the your input..."}

    @staticmethod
    @tool
    async def executeAPI(url: str, method='GET', payload={}, message="") -> str:
        """Execute the API call and return the response text."""
        username = AirflowTools._env.airflow_user_name
        password = AirflowTools._env.airflow_user_pass

        try:
            async with httpx.AsyncClient() as client:
                if method == "POST":
                    response = await client.post(url, auth=(username, password), json=payload)
                elif method == "GET":
                    response = await client.get(url, auth=(username, password))
                elif method == "PATCH":
                    response = await client.patch(url, auth=(username, password), json=payload)
                elif url is None and method is None and str(message).strip() != "":
                    return message
                else:
                    raise ValueError(f"Unsupported method: {method}")
            return response.text
        except httpx.RequestError as e:
            return f"❌ Error: {e}"
        
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
            # cls.connection_test,
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
            cls.list_dataset_triggered_dags,
            cls.executeAPI
        ]
