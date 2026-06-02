#!/usr/bin/env bash
#
# trello.sh — minimal Trello REST API client for macOS / Linux (and any
# POSIX shell with curl available, e.g. Git Bash / WSL on Windows).
#
# Usage:
#   scripts/trello.sh <METHOD> <PATH[?query]> [--data '<json>'] [extra curl args...]
#
# Examples:
#   scripts/trello.sh GET  "/members/me/boards?fields=name,url"
#   scripts/trello.sh POST "/cards?idList=<listId>&name=Hello"
#   scripts/trello.sh PUT  "/cards/<id>" --data '{"name":"Renamed"}'
#   scripts/trello.sh DELETE "/cards/<id>"
#
# Auth is read from environment variables:
#   TRELLO_API_KEY    (required)
#   TRELLO_API_TOKEN  (required; TRELLO_TOKEN is accepted as a fallback)
#
# The base URL can be overridden with TRELLO_API_BASE
# (default: https://api.trello.com/1).
#
# The script auto-appends key & token to the query string, so never put them
# in <PATH> yourself. It prints the raw response body to stdout and exits
# non-zero on HTTP >= 400.

set -euo pipefail

BASE_URL="${TRELLO_API_BASE:-https://api.trello.com/1}"
KEY="${TRELLO_API_KEY:-}"
TOKEN="${TRELLO_API_TOKEN:-${TRELLO_TOKEN:-}}"

err() { printf '%s\n' "$*" >&2; }

if ! command -v curl >/dev/null 2>&1; then
  err "curl not found. Install it first:"
  err "  scripts/ensure-curl.sh"
  exit 127
fi

if [ "$#" -lt 2 ]; then
  err "Usage: trello.sh <METHOD> <PATH[?query]> [--data '<json>'] [curl args...]"
  exit 2
fi

if [ -z "$KEY" ] || [ -z "$TOKEN" ]; then
  err "Missing credentials. Set TRELLO_API_KEY and TRELLO_API_TOKEN."
  err "See references/authentication.md for how to obtain and export them."
  exit 3
fi

METHOD="$(printf '%s' "$1" | tr '[:lower:]' '[:upper:]')"
RAW_PATH="$2"
shift 2

# Split off an existing query string so we can append auth params.
case "$RAW_PATH" in
  *\?*) PATH_PART="${RAW_PATH%%\?*}"; QUERY_PART="${RAW_PATH#*\?}" ;;
  *)    PATH_PART="$RAW_PATH"; QUERY_PART="" ;;
esac

AUTH="key=${KEY}&token=${TOKEN}"
if [ -n "$QUERY_PART" ]; then
  QUERY="${QUERY_PART}&${AUTH}"
else
  QUERY="$AUTH"
fi

# Ensure leading slash on the path.
case "$PATH_PART" in
  /*) : ;;
  *) PATH_PART="/${PATH_PART}" ;;
esac

URL="${BASE_URL}${PATH_PART}?${QUERY}"

# If a JSON body is supplied via --data, send the proper content type.
HAS_DATA=0
for arg in "$@"; do
  case "$arg" in
    --data|--data-raw|-d|--data-binary) HAS_DATA=1 ;;
  esac
done

if [ "$HAS_DATA" -eq 1 ]; then
  exec curl -sS --fail-with-body -X "$METHOD" "$URL" \
    -H "Content-Type: application/json" "$@"
else
  exec curl -sS --fail-with-body -X "$METHOD" "$URL" "$@"
fi
