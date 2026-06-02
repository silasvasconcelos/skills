# Trello API — Batch

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Batch runs up to 10 API routes in one request;
each route in `urls` must start with `/`.

## GET /batch — Batch Requests
Query params: `urls` (required; comma-separated API paths, max 10).

```bash
scripts/trello.sh GET "/batch?urls=/members/me,/boards/<id>"
```
