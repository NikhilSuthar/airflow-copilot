import logging as logs
import psycopg
from typing import Optional, Tuple
from airflow_copilot.config.settings import get_environment
from airflow_copilot.config.settings import user_id_context
import httpx
import datetime

import os


logs = logs.getLogger(__name__)
env = get_environment()



def get_connection():
    return psycopg.connect(env.db_uri)


async def get_user_credentials(thread_id: str) -> Optional[Tuple[str, str]]:
    """Fetch encrypted user credentials by thread_id and decrypt."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT airflow_username, airflow_password FROM user_credentials WHERE thread_id = %s",
                    (thread_id,)
                )
                row = cur.fetchone()
                if row:
                    username, encrypted_password = row
                    decrypted_password = env.decrypt_password(encrypted_password)
                    return username, decrypted_password
                else:
                    logs.warning(f"No credentials found for User ={thread_id}")
                    return None,None
    except Exception as e:
        logs.error(f"❌ Error fetching credentials: {e}")
        return None,None
    

async def save_user_credentials(thread_id: str, username: str, password: str) -> bool:
    """Store encrypted credentials. Overwrites if already exists."""
    try:
        encrypted = env.encrypt_password(password)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO  user_credentials (thread_id, airflow_username, airflow_password)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (thread_id) DO UPDATE
                    SET airflow_username = EXCLUDED.airflow_username,
                        airflow_password = EXCLUDED.airflow_password,
                        created_at = NOW()
                    """,
                    (thread_id, username, encrypted)
                )
        logs.debug(f"Saved credentials for thread_id={thread_id}")
        return True
    except Exception as e:
        logs.error(f"Error saving credentials for thread_id={thread_id}: {e}")
        return False

    
@staticmethod
async def test_credential(user_id:str) -> str:
    try:
        (username,password) = await get_user_credentials(thread_id=user_id)
        async with httpx.AsyncClient() as client:
            url = f"{env.airflow_base_url}/dags"
            response = await client.get(url, auth=(username, password))
            logs.debug(f"Credential Testing Response - {response}")
            if response.status_code == 200:
                logs.info(f"User {user_id} credential are valid.")
                return f"Success"
            else:
                logs.warning(f"User {user_id} credential are Invalid.")
                return f"Failed|{response}"
    except Exception as e:
        logs.error(e)
        return f"Failed|{e}"
    

  