#!/bin/sh

echo "🔁 Waiting for Copilot to be ready..."
until curl -sf http://copilot:3978/health > /dev/null; do
  echo "⏳ Copilot not ready yet..."
  sleep 3
done

echo "✅ Copilot is up! Starting ngrok..."
exec ngrok http copilot:3978 --log stdout