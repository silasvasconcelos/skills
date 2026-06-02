# Trello API — Custom Fields

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Custom fields are board-level definitions used on
cards (text, number, date, checkbox, or dropdown).

## POST /customFields — Create a new Custom Field on a Board
Request body (JSON): `idModel` (required), `modelType` (required), `name` (required), `type` (required), `pos` (required), `options`, `display_cardFront` (optional).

```bash
scripts/trello.sh POST "/customFields"
```

## GET /customFields/{id} — Get a Custom Field
```bash
scripts/trello.sh GET "/customFields/<id>"
```

## PUT /customFields/{id} — Update a Custom Field definition
Request body (JSON): `name`, `pos`, `display/cardFront` (all optional).

```bash
scripts/trello.sh PUT "/customFields/<id>"
```

## DELETE /customFields/{id} — Delete a Custom Field definition
```bash
scripts/trello.sh DELETE "/customFields/<id>"
```

## POST /customFields/{id}/options — Add Option to Custom Field dropdown
Path params: `id` (required).

```bash
scripts/trello.sh POST "/customFields/<id>/options"
```

## GET /customFields/{id}/options — Get Options of Custom Field drop down
```bash
scripts/trello.sh GET "/customFields/<id>/options"
```

## GET /customFields/{id}/options/{idCustomFieldOption} — Get Option of Custom Field dropdown
```bash
scripts/trello.sh GET "/customFields/<id>/options/<idCustomFieldOption>"
```

## DELETE /customFields/{id}/options/{idCustomFieldOption} — Delete Option of Custom Field dropdown
```bash
scripts/trello.sh DELETE "/customFields/<id>/options/<idCustomFieldOption>"
```
