#!/usr/bin/env bash
set -euo pipefail

# Starts Kestra locally for HW3, pulling the Gemini API key from 1Password
# so it never touches disk or shell history in plaintext.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCHESTRATION_DIR="${ORCHESTRATION_DIR:-$SCRIPT_DIR/..}"
OP_ITEM_GEMINI="${OP_ITEM_GEMINI:-GeminiDataTalk}"
OP_ITEM_TAVILY="${OP_ITEM_TAVILY:-6roxnxry7f37o7qwcsvdi3eqmu}"

if ! command -v op >/dev/null 2>&1; then
  echo "1Password CLI ('op') not found. Install it or export GEMINI_API_KEY manually." >&2
  exit 1
fi

export GEMINI_API_KEY
GEMINI_API_KEY="$(op item get "$OP_ITEM_GEMINI" --fields credential --reveal)"
export SECRET_GEMINI_API_KEY
SECRET_GEMINI_API_KEY="$(echo -n "$GEMINI_API_KEY" | base64)"

export SECRET_TAVILY_API_KEY
SECRET_TAVILY_API_KEY="$(op item get "$OP_ITEM_TAVILY" --fields credential --reveal | base64)"

cd "$ORCHESTRATION_DIR"
docker compose up -d

echo "Waiting for Kestra to respond on http://localhost:8080 ..."
until curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 | grep -qE '^(2|3)[0-9]{2}$'; do
  sleep 2
done
echo "Kestra is up: http://localhost:8080"
