import os
import logging as logs
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv, set_key
from functools import lru_cache
from typing import Optional
import contextvars

# ────────────────────────── Logging Setup ──────────────────────────
logs.basicConfig(
    level=logs.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# ────────────────────────── Optional .env Loading ──────────────────────────
ENV_PATH = "/app/src/.env"
load_dotenv(dotenv_path=ENV_PATH, override=True)
logs.info(f"✅ Loading .env from {ENV_PATH}")

# ────────────────────────── App Settings ──────────────────────────
class Settings:
    def __init__(self):
        # LLM Details
        self.provider_name = os.getenv("LLM_MODEL_PROVIDER_NAME")
        self.model_name = os.getenv("LLM_MODEL_NAME")
        self.api_key = os.getenv(f"{str(self.provider_name).upper()}_API_KEY", "")

        # Azure BOT
        self.microsoft_app_id = os.getenv("MICROSOFT_APP_ID")
        self.microsoft_app_password = os.getenv("MICROSOFT_APP_PASSWORD")

        # Checkpointer Details
        self.db_uri = os.getenv("DB_URI")

        # Summarization Threshold
        self.summarization_provider_name = self.provider_name if str(os.getenv("SUMMARIZATION_LLM_MODEL_PROVIDER_NAME", "")).strip() == "" else os.getenv("SUMMARIZATION_LLM_MODEL_PROVIDER_NAME")
        self.summarization_model_name = self.model_name if str(os.getenv("SUMMARIZATION_LLM_MODEL_NAME", "")).strip() == "" else os.getenv("SUMMARIZATION_LLM_MODEL_NAME")
        self.summarization_api_key = os.getenv(f"{str(self.summarization_provider_name).upper()}_API_KEY", "")
        self.min_msg_to_retain = self._parse_threshold(os.getenv("MIN_MSG_TO_RETAIN"))
        self.min_msg_to_summarize = self._parse_threshold(os.getenv("MIN_MSG_TO_SUMMARIZE"))

        # Airflow Auth Strategy
        self.auth_strategy = os.getenv("AIRFLOW_AUTH_STRATEGY", "per_user").strip().lower()
        self.bot_name = os.getenv("AZURE_BOT_NAME", "Airflow‑Copilot").strip().lower()

        # Airflow Centralized Auth
        self.airflow_base_url = os.getenv("AIRFLOW_BASE_URL", "").rstrip("/")
        if not self.airflow_base_url.endswith("/api/v1"):
            self.airflow_base_url += "/api/v1"
        self.airflow_user_name = os.getenv("AIRFLOW_USER_NAME")
        self.airflow_user_pass = os.getenv("AIRFLOW_USER_PASSWORD")

        # Fernet Key (used only in per_user mode)
        self.fernet_secret_key = os.getenv("FERNET_SECRET_KEY")
        self._fernet = Fernet(self.fernet_secret_key.encode()) if self.fernet_secret_key else None

        self.validate()

    def _parse_threshold(self, value: Optional[str]) -> Optional[int]:
        """Convert string to int. Treat 0 or invalid as None."""
        try:
            v = int(value)
            return v if v >= 0 else 10
        except (ValueError, TypeError):
            return 10

    def validate(self):
        """Ensure required variables are present."""
        missing = []
        mandatory_variables = [
            "LLM_MODEL_PROVIDER_NAME", "LLM_MODEL_NAME", "DB_URI",
            "AIRFLOW_BASE_URL", "MICROSOFT_APP_ID", "MICROSOFT_APP_PASSWORD"
        ]

        for var in mandatory_variables:
            if not os.getenv(var):
                missing.append(var)

        if self.auth_strategy == "centralized":
            if not self.airflow_user_name:
                missing.append("AIRFLOW_USER_NAME")
            if not self.airflow_user_pass:
                missing.append("AIRFLOW_USER_PASSWORD")
        elif self.auth_strategy == "per_user":
            if not self.fernet_secret_key:
                missing.append("FERNET_SECRET_KEY")
        else:
            missing.append("AIRFLOW_AUTH_STRATEGY")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        else:
            logs.info(f"✅ All required environment variables are present.")

    def encrypt_password(self, password: str) -> str:
        if not self._fernet:
            raise ValueError("FERNET_SECRET_KEY is missing or invalid.")
        return self._fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted: str) -> str:
        if not self._fernet:
            raise ValueError("FERNET_SECRET_KEY is missing or invalid.")
        return self._fernet.decrypt(encrypted.encode()).decode()


# ────────────────────────── Global Singleton ──────────────────────────
user_id_context = contextvars.ContextVar("user_id")

@lru_cache()
def get_environment() -> Settings:
    print(f"Environment Variables are ----------------------------------------")
    print(Settings())
    print("---------------------------------------------------------------------")
    return Settings()

