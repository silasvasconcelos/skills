# Trello API — Applications

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Application endpoints expose compliance data for
your Trello API key.

## GET /applications/{key}/compliance — Get Application's compliance data
Path params: `key` (required).

```bash
scripts/trello.sh GET "/applications/<key>/compliance"
```
