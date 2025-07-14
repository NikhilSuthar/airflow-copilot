#!/usr/bin/env bash
# ------------------------------------------------------------
# init-copilot.sh
#
# • Wait for Postgres (via $DB_URI)
# • Run /init.sql (must be baked into the image)
# ------------------------------------------------------------
set -euo pipefail

: "${DB_URI:?DB_URI env var must be set (e.g. postgresql://user:pass@host:5432/db)}"



RETRY_INTERVAL=3
MAX_WAIT=10
elapsed=1
elapsed_time=$RETRY_INTERVAL
MAX_TIME=$(( $RETRY_INTERVAL * $MAX_WAIT ))
echo "🗄️  Waiting for Postgres at $DB_URI ($MAX_TIME seconds max)…"

until psql "$DB_URI" -c 'SELECT 1;' >/dev/null 2>&1; do
  if (( elapsed >= MAX_WAIT )); then
    echo "❌ Postgres not reachable after $MAX_TIME seconds. Aborting."
    exit 1
  fi
  elapsed_time=$(( $RETRY_INTERVAL * $elapsed ))
  echo "❌ Postgres not reachable after $elapsed_time seconds. Retrying... $elapsed"
  sleep $RETRY_INTERVAL
  (( elapsed += 1 ))
done

echo "✅ Postgres is reachable."

if [[ ! -f /usr/local/bin/init.sql ]]; then
  echo "❌ /usr/local/bin/init.sql not found inside the image. Abort."
  exit 1
fi

echo "▶️  Applying schema from /usr/local/bin/init.sql"
psql "$DB_URI" -v ON_ERROR_STOP=1 -f /usr/local/bin/init.sql
echo "🎉 Database bootstrap complete."
