# Trello API — Emoji

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Emoji endpoints list available emoji for
reactions and comments.

## GET /emoji — List available Emoji
Query params (all optional): `locale`, `spritesheets` (bool).

```bash
scripts/trello.sh GET "/emoji?locale=en&spritesheets=true"
```
