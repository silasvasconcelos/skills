# Trello API — Labels

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Labels are colored tags on a board, attachable
to cards.

## POST /labels — Create a Label
Query params: `name` (required), `color` (required), `idBoard` (required).

```bash
scripts/trello.sh POST "/labels?name=Bug&color=red&idBoard=<boardId>"
```

## GET /labels/{id} — Get a Label
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/labels/<id>?fields=name,color"
```

## PUT /labels/{id} — Update a Label
Query params (all optional): `name`, `color`.

```bash
scripts/trello.sh PUT "/labels/<id>?name=Critical&color=orange"
```

## DELETE /labels/{id} — Delete a Label
```bash
scripts/trello.sh DELETE "/labels/<id>"
```

## PUT /labels/{id}/{field} — Update a field on a label
Path params: `id` (required), `field` (required). Query params: `value` (required).

```bash
scripts/trello.sh PUT "/labels/<id>/name?value=Renamed"
```
