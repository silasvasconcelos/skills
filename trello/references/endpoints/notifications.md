# Trello API — Notifications

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Notifications are activity alerts for the
authenticated member.

## POST /notifications/all/read — Mark all Notifications as read
Query params (all optional): `read` (bool; default marks read), `ids` (comma-separated notification IDs).

```bash
scripts/trello.sh POST "/notifications/all/read?read=true"
```

## GET /notifications/{id} — Get a Notification
Path params: `id` (required). Query params (all optional): `board`, `board_fields`, `card`, `card_fields`, `display`, `entities`, `fields`, `list`, `member`, `member_fields`, `memberCreator`, `memberCreator_fields`, `organization`, `organization_fields`.

```bash
scripts/trello.sh GET "/notifications/<id>?fields=type,date,unread"
```

## PUT /notifications/{id} — Update a Notification's read status
Path params: `id` (required). Query params: `unread` (optional).

```bash
scripts/trello.sh PUT "/notifications/<id>?unread=false"
```

## GET /notifications/{id}/{field} — Get a field of a Notification
Path params: `id` (required), `field` (required).

```bash
scripts/trello.sh GET "/notifications/<id>/unread"
```

## PUT /notifications/{id}/unread — Update Notification's read status
Path params: `id` (required). Query params: `value` (optional).

```bash
scripts/trello.sh PUT "/notifications/<id>/unread?value=false"
```

## GET /notifications/{id}/board — Get the Board a Notification is on
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/board?fields=name"
```

## GET /notifications/{id}/card — Get the Card a Notification is on
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/card?fields=name"
```

## GET /notifications/{id}/list — Get the List a Notification is on
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/list?fields=name"
```

## GET /notifications/{id}/member — Get the Member a Notification is about (not the creator)
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/member?fields=fullName"
```

## GET /notifications/{id}/memberCreator — Get the Member who created the Notification
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/memberCreator?fields=fullName"
```

## GET /notifications/{id}/organization — Get a Notification's associated Organization
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/notifications/<id>/organization?fields=displayName"
```
