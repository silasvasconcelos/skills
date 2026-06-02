# Trello API — Checklists

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Checklists group check items on a card; use
card-scoped endpoints to attach a checklist to a specific card.

## POST /checklists — Create a Checklist
Query params: `idCard` (required), `name`, `pos`, `idChecklistSource`.

```bash
scripts/trello.sh POST "/checklists?idCard=<cardId>"
```

## GET /checklists/{id} — Get a Checklist
Path params: `id` (required).
Query params (all optional): `cards`, `checkItems`, `checkItem_fields`, `fields`.

```bash
scripts/trello.sh GET "/checklists/<id>?cards=all"
```

## PUT /checklists/{id} — Update a Checklist
Path params: `id` (required).
Query params (all optional): `name`, `pos`.

```bash
scripts/trello.sh PUT "/checklists/<id>?name=My%20checklist"
```

## DELETE /checklists/{id} — Delete a Checklist
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/checklists/<id>"
```

## GET /checklists/{id}/board — Get the Board the Checklist is on
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/checklists/<id>/board?fields=name,desc"
```

## GET /checklists/{id}/cards — Get the Card a Checklist is on
Path params: `id` (required).

```bash
scripts/trello.sh GET "/checklists/<id>/cards"
```

## GET /checklists/{id}/checkItems — Get Checkitems on a Checklist
Path params: `id` (required).
Query params (all optional): `filter`, `fields`.

```bash
scripts/trello.sh GET "/checklists/<id>/checkItems?filter=all"
```

## POST /checklists/{id}/checkItems — Create Checkitem on Checklist
Path params: `id` (required).
Query params: `name` (required), `pos`, `checked`, `due`, `dueReminder`, `idMember`.

```bash
scripts/trello.sh POST "/checklists/<id>/checkItems?name=My%20card"
```

## GET /checklists/{id}/checkItems/{idCheckItem} — Get a Checkitem on a Checklist
Path params: `id` (required), `idCheckItem` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/checklists/<id>/checkItems/<checkItemId>?fields=name,desc"
```

## DELETE /checklists/{id}/checkItems/{idCheckItem} — Delete Checkitem from Checklist
Path params: `id` (required), `idCheckItem` (required).

```bash
scripts/trello.sh DELETE "/checklists/<id>/checkItems/<checkItemId>"
```

## GET /checklists/{id}/{field} — Get field on a Checklist
Path params: `id` (required), `field` (required).
Path `field`: name, pos, etc.

```bash
scripts/trello.sh GET "/checklists/<id>/<field>"
```

## PUT /checklists/{id}/{field} — Update field on a Checklist
Path params: `id` (required), `field` (required).
Path `field`: name, pos, etc.
Query params: `value` (required).

```bash
scripts/trello.sh PUT "/checklists/<id>/<field>?value=My%20checklist"
```
