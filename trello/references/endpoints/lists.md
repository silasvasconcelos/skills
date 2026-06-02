# Trello API — Lists

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Lists are columns on a board containing cards.

## POST /lists — Create a new List
Query params: `name` (required), `idBoard` (required), `idListSource`, `pos` (optional).

```bash
scripts/trello.sh POST "/lists?name=To%20Do&idBoard=<boardId>&pos=top"
```

## GET /lists/{id} — Get a List
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/lists/<id>?fields=name,closed,pos"
```

## PUT /lists/{id} — Update a List
Query params (all optional): `name`, `closed`, `idBoard`, `pos`, `subscribed`.

```bash
scripts/trello.sh PUT "/lists/<id>?name=In%20Progress&closed=false"
```

## GET /lists/{id}/actions — Get Actions for a List
Path params: `id` (required). Query params: `filter` (optional).

```bash
scripts/trello.sh GET "/lists/<id>/actions?filter=createCard,updateCard"
```

## POST /lists/{id}/archiveAllCards — Archive all Cards in List
Path params: `id` (required).

```bash
scripts/trello.sh POST "/lists/<id>/archiveAllCards"
```

## GET /lists/{id}/board — Get the Board a List is on
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/lists/<id>/board?fields=name,url"
```

## GET /lists/{id}/cards — Get Cards in a List
Path params: `id` (required).

```bash
scripts/trello.sh GET "/lists/<id>/cards"
```

## PUT /lists/{id}/closed — Archive or unarchive a list
Path params: `id` (required). Query params: `value` (optional; `true` to archive).

```bash
scripts/trello.sh PUT "/lists/<id>/closed?value=true"
```

## PUT /lists/{id}/idBoard — Move List to Board
Path params: `id` (required). Query params: `value` (required; target board ID).

```bash
scripts/trello.sh PUT "/lists/<id>/idBoard?value=<boardId>"
```

## POST /lists/{id}/moveAllCards — Move all Cards in List
Path params: `id` (required). Query params: `idBoard` (required), `idList` (required).

```bash
scripts/trello.sh POST "/lists/<id>/moveAllCards?idBoard=<boardId>&idList=<listId>"
```

## PUT /lists/{id}/{field} — Update a field on a List
Path params: `id` (required), `field` (required). Query params: `value` (optional).

```bash
scripts/trello.sh PUT "/lists/<id>/name?value=Done"
```
