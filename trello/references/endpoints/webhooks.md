# Trello API — Webhooks

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Webhooks fire a `POST`/`HEAD` to your
`callbackURL` whenever the watched model changes — prefer them over polling.

## POST /webhooks/ — Create a webhook
Query params: `callbackURL` (required), `idModel` (required), `description`, `active` (bool).

```bash
scripts/trello.sh POST "/webhooks/?callbackURL=https%3A%2F%2Fexample.com%2Fhook&idModel=<modelId>&description=My%20hook"
```

## GET /webhooks/{id} — Get a webhook
```bash
scripts/trello.sh GET "/webhooks/<id>"
```

## PUT /webhooks/{id} — Update a webhook
Query params (all optional): `callbackURL`, `idModel`, `description`, `active`.

```bash
scripts/trello.sh PUT "/webhooks/<id>?active=false"
```

## DELETE /webhooks/{id} — Delete a webhook
```bash
scripts/trello.sh DELETE "/webhooks/<id>"
```

## GET /webhooks/{id}/{field} — Get one field of a webhook
Path `field` is one of: `active`, `callbackURL`, `description`, `idModel`.

```bash
scripts/trello.sh GET "/webhooks/<id>/active"
```
