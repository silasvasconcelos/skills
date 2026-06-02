# Trello API — Tokens

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Token endpoints manage the active API token and
its webhooks.

## GET /tokens/{token} — Get a Token
Query params (all optional): `fields`, `webhooks`.

```bash
scripts/trello.sh GET "/tokens/<token>?fields=dateCreated,idMember"
```

## DELETE /tokens/{token}/ — Delete a Token
```bash
scripts/trello.sh DELETE "/tokens/<token>/"
```

## GET /tokens/{token}/member — Get Token's Member
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/tokens/<token>/member?fields=fullName,username"
```

## GET /tokens/{token}/webhooks — Get Webhooks for Token
```bash
scripts/trello.sh GET "/tokens/<token>/webhooks"
```

## POST /tokens/{token}/webhooks — Create Webhooks for Token
Query params: `callbackURL` (required), `idModel` (required), `description` (optional).

```bash
scripts/trello.sh POST "/tokens/<token>/webhooks?callbackURL=https%3A%2F%2Fexample.com%2Fhook&idModel=<modelId>"
```

## GET /tokens/{token}/webhooks/{idWebhook} — Get a Webhook belonging to a Token
```bash
scripts/trello.sh GET "/tokens/<token>/webhooks/<idWebhook>"
```

## PUT /tokens/{token}/webhooks/{idWebhook} — Update a Webhook created by Token
Query params (all optional): `description`, `callbackURL`, `idModel`.

```bash
scripts/trello.sh PUT "/tokens/<token>/webhooks/<idWebhook>?description=Updated%20hook"
```

## DELETE /tokens/{token}/webhooks/{idWebhook} — Delete a Webhook created by Token
```bash
scripts/trello.sh DELETE "/tokens/<token>/webhooks/<idWebhook>"
```
