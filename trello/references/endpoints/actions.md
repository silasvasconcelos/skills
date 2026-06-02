# Trello API — Actions

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Action list endpoints return at most 1000 items;
page with `before` and `since` (e.g. on board, card, or list action lists).

## GET /actions/{id} — Get an Action
Query params (all optional): `display`, `entities`, `fields`, `member`, `member_fields`, `memberCreator`, `memberCreator_fields`.

```bash
scripts/trello.sh GET "/actions/<id>?fields=data,type,date"
```

## PUT /actions/{id} — Update an Action
Query params: `text` (required).

```bash
scripts/trello.sh PUT "/actions/<id>?text=Updated%20comment"
```

## DELETE /actions/{id} — Delete an Action
```bash
scripts/trello.sh DELETE "/actions/<id>"
```

## GET /actions/{id}/{field} — Get a specific field on an Action
Path params: `id` (required), `field` (required).

```bash
scripts/trello.sh GET "/actions/<id>/type"
```

## GET /actions/{id}/board — Get the Board for an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/board?fields=name,url"
```

## GET /actions/{id}/card — Get the Card for an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/card?fields=name,desc"
```

## GET /actions/{id}/list — Get the List for an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/list?fields=name"
```

## GET /actions/{id}/member — Get the Member of an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/member?fields=fullName,username"
```

## GET /actions/{id}/memberCreator — Get the Member Creator of an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/memberCreator?fields=fullName"
```

## GET /actions/{id}/organization — Get the Organization of an Action
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/actions/<id>/organization?fields=displayName"
```

## PUT /actions/{id}/text — Update a Comment Action
Path params: `id` (required). Query params: `value` (required).

```bash
scripts/trello.sh PUT "/actions/<id>/text?value=New%20comment%20text"
```

## GET /actions/{idAction}/reactions — Get Action's Reactions
Query params (all optional): `member`, `emoji`.

```bash
scripts/trello.sh GET "/actions/<idAction>/reactions"
```

## POST /actions/{idAction}/reactions — Create Reaction for Action
Request body (JSON): `shortName`, `skinVariation`, `native`, `unified` (all optional).

```bash
scripts/trello.sh POST "/actions/<idAction>/reactions"
```

## GET /actions/{idAction}/reactions/{id} — Get Action's Reaction
Query params (all optional): `member`, `emoji`.

```bash
scripts/trello.sh GET "/actions/<idAction>/reactions/<id>"
```

## DELETE /actions/{idAction}/reactions/{id} — Delete Action's Reaction
```bash
scripts/trello.sh DELETE "/actions/<idAction>/reactions/<id>"
```

## GET /actions/{idAction}/reactionsSummary — List Action's summary of Reactions
Path params: `idAction` (required).

```bash
scripts/trello.sh GET "/actions/<idAction>/reactionsSummary"
```
