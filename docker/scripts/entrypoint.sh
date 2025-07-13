#!/usr/bin/env bash
set -euo pipefail

# ---------- unconditional vars ----------
: "${LLM_MODEL_PROVIDER_NAME?Need LLM_MODEL_PROVIDER_NAME}"
: "${AIRFLOW_BASE_URL?Need AIRFLOW_BASE_URL}"
: "${FERNET_SECRET_KEY?Need FERNET_SECRET_KEY}"

# ---------- conditional checks ----------
case "${LLM_MODEL_PROVIDER_NAME}" in
  Google_Genai)
    : "${GOOGLE_GENAI_API_KEY?GOOGLE_GENAI_API_KEY must be set for Google_Genai}"
    ;;
  OpenAI)
    : "${OPENAI_API_KEY?OPENAI_API_KEY must be set for OpenAI}"
    ;;
  Anthropic)
    : "${ANTHROPIC_API_KEY?ANTHROPIC_API_KEY must be set for Anthropic}"
    ;;
  Groq)
    : "${GROQ_API_KEY?GROQ_API_KEY must be set for Groq}"
    ;;
  *)
    echo "❌ Unsupported LLM_MODEL_PROVIDER_NAME: ${LLM_MODEL_PROVIDER_NAME}" >&2
    exit 1
    ;;
esac

# ---------- launch uvicorn ----------
exec "$@"
