#!/bin/bash

# === CONFIGURATION ===
PORT=3978
NGROK_LOG_FILE=ngrok.log
FASTAPI_FILE="airflow_copilot.app.app"
BOT_NAME="AirflowCopilot"
RESOURCE_GROUP="my-rg"

echo "⚠️ Force kill anything on that port (optional, not recommended for production)"
lsof -ti tcp:$PORT | xargs kill -9
# === START FASTAPI ===
echo "🚀 Starting FastAPI on port $PORT..."
uvicorn $FASTAPI_FILE:app --host 0.0.0.0 --port $PORT --reload --log-level info &
FASTAPI_PID=$!

# === START NGROK ===
echo "🔗 Starting ngrok..."
ngrok http $PORT --host-header="localhost:$PORT" > "$NGROK_LOG_FILE" &
NGROK_PID=$!

sleep 5

# # === EXTRACT NGROK URL ===
# NGROK_URL=$(curl -s https://localhost:4040/api/tunnels \
#   | grep -o 'https://[a-z0-9]*\.ngrok' \
#   | head -n 1)~
NGROK_URL=$(python ./get_ngrok_url.py)
echo "🚀 Extracted NGROK URL is -->  $NGROK_URL"

if [ -z "$NGROK_URL" ]; then
  echo "❌ Failed to get ngrok URL."
else
  echo "✅ ngrok public URL: $NGROK_URL"

  FULL_URL="${NGROK_URL}/api/messages"

  echo "🔄 Updating Azure Bot endpoint to $FULL_URL..."
  az bot update \
    --name "$BOT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --endpoint "$FULL_URL"

  if [ $? -eq 0 ]; then
    echo "✅ Azure Bot endpoint updated successfully."
  else
    echo "❌ Failed to update Azure Bot endpoint."
  fi
fi

# === CLEANUP ON EXIT ===
trap "echo '🛑 Stopping...'; kill $FASTAPI_PID $NGROK_PID; exit" SIGINT

wait
