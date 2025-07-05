#!/usr/bin/env bash
set -euo pipefail

########################################
# 0)  Config & sanity checks
########################################
: "${AZURE_CLIENT_ID:?Need AZURE_CLIENT_ID}"
: "${AZURE_CLIENT_SECRET:?Need AZURE_CLIENT_SECRET}"
: "${AZURE_TENANT_ID:?Need AZURE_TENANT_ID}"
: "${BOT_NAME:?Need BOT_NAME}"
: "${RESOURCE_GROUP:?Need RESOURCE_GROUP}"
: "${NGROK_API:?Need NGROK_API}"


########################################
# 2)  Azure Login
########################################
echo "🔐 Logging into Azure with SPN $AZURE_CLIENT_ID"
az login --service-principal -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" --tenant "$AZURE_TENANT_ID"

########################################
# 3)  Wait for ngrok HTTPS tunnel
########################################
echo "⏳ Waiting for ngrok tunnel to appear..."
until curl -s "$NGROK_API" | grep -q '"proto":"https"'; do sleep 2; done
PUBLIC_URL=$(curl -s "$NGROK_API" | grep -oE 'https://[^"]+' | head -n 1)
FULL_ENDPOINT="${PUBLIC_URL}/api/messages"
echo "🌐 Tunnel URL: $FULL_ENDPOINT"

########################################
# 4)  Patch Azure Bot endpoint
########################################
echo "🔄 Patching Azure Bot endpoint..."
az bot update --name "$BOT_NAME" --resource-group "$RESOURCE_GROUP" --endpoint "$FULL_ENDPOINT"
echo "🚀 Init finished."
