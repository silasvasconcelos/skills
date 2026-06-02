# Trello API — Cards

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Cards are the primary work items on a board —
create, update, and manage attachments, checklists, labels, and members on them.

## POST /cards — Create a new Card
Query params: `idList` (required), `name`, `desc`, `pos`, `due`, `start`, `dueComplete`, `idMembers`, `idLabels`, `urlSource`, `fileSource`, `mimeType`, `idCardSource`, `keepFromSource`, `address`, `locationName`, `coordinates`, `cardRole`.

```bash
scripts/trello.sh POST "/cards?idList=<listId>&name=My%20card"
```

## PUT /cards/{idCard}/checklist/{idChecklist}/checkItem/{idCheckItem} — Update Checkitem on Checklist on Card
Path params: `idCard` (required), `idCheckItem` (required), `idChecklist` (required).
Query params (all optional): `pos`.

```bash
scripts/trello.sh PUT "/cards/<cardId>/checklist/<checklistId>/checkItem/<checkItemId>?pos=top"
```

## PUT /cards/{idCard}/customField/{idCustomField}/item — Update Custom Field item on Card
Path params: `idCard` (required), `idCustomField` (required).
Request body (JSON): `{ "value": { ... } }` or `{ "idValue": "<optionId>" }` for list-type fields.

```bash
scripts/trello.sh PUT "/cards/<cardId>/customField/<customFieldId>/item" --data '{"value":{"text":"Done"}}'
```

## PUT /cards/{idCard}/customFields — Update Multiple Custom Field items on Card
Path params: `idCard` (required).
Request body (JSON): `{ "customFieldItems": [ { "idCustomField", "value" | "idValue" } ] }`.

```bash
scripts/trello.sh PUT "/cards/<cardId>/customFields" --data '{"customFieldItems":[{"idCustomField":"<customFieldId>","value":{"text":"Done"}}]}'
```

## GET /cards/{id} — Get a Card
Path params: `id` (required).
Query params (all optional): `fields`, `actions`, `attachments`, `attachment_fields`, `members`, `member_fields`, `membersVoted`, `memberVoted_fields`, `checkItemStates`, `checklists`, `checklist_fields`, `board`, `board_fields`, `list`, `pluginData`, `stickers`, `sticker_fields`, `customFieldItems`.

```bash
scripts/trello.sh GET "/cards/<id>?fields=name,desc"
```

## PUT /cards/{id} — Update a Card
Path params: `id` (required).
Query params (all optional): `name`, `desc`, `closed`, `idMembers`, `idAttachmentCover`, `idList`, `idLabels`, `idBoard`, `pos`, `due`, `start`, `dueComplete`, `subscribed`, `address`, `locationName`, `coordinates`, `cover`.

```bash
scripts/trello.sh PUT "/cards/<id>?name=My%20card"
```

## DELETE /cards/{id} — Delete a Card
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>"
```

## GET /cards/{id}/actions — Get Actions on a Card
Path params: `id` (required).
Query params (all optional): `filter`, `page`.

```bash
scripts/trello.sh GET "/cards/<id>/actions?filter=all"
```

## POST /cards/{id}/actions/comments — Add a new comment to a Card
Path params: `id` (required).
Query params: `text` (required).

```bash
scripts/trello.sh POST "/cards/<id>/actions/comments?text=Comment"
```

## PUT /cards/{id}/actions/{idAction}/comments — Update Comment Action on a Card
Path params: `id` (required), `idAction` (required).
Query params: `text` (required).

```bash
scripts/trello.sh PUT "/cards/<id>/actions/<actionId>/comments?text=Comment"
```

## DELETE /cards/{id}/actions/{idAction}/comments — Delete a comment on a Card
Path params: `id` (required), `idAction` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/actions/<actionId>/comments"
```

## GET /cards/{id}/attachments — Get Attachments on a Card
Path params: `id` (required).
Query params (all optional): `fields`, `filter`.

```bash
scripts/trello.sh GET "/cards/<id>/attachments?fields=name,desc"
```

## POST /cards/{id}/attachments — Create Attachment On Card
Path params: `id` (required).
Query params (all optional): `name`, `file`, `mimeType`, `url`, `setCover`.

```bash
scripts/trello.sh POST "/cards/<id>/attachments?name=My%20card"
```

## GET /cards/{id}/attachments/{idAttachment} — Get an Attachment on a Card
Path params: `id` (required), `idAttachment` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/attachments/<attachmentId>?fields=name,desc"
```

## DELETE /cards/{id}/attachments/{idAttachment} — Delete an Attachment on a Card
Path params: `id` (required), `idAttachment` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/attachments/<attachmentId>"
```

## GET /cards/{id}/board — Get the Board the Card is on
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/board?fields=name,desc"
```

## GET /cards/{id}/checkItem/{idCheckItem} — Get checkItem on a Card
Path params: `id` (required), `idCheckItem` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/checkItem/<checkItemId>?fields=name,desc"
```

## PUT /cards/{id}/checkItem/{idCheckItem} — Update a checkItem on a Card
Path params: `id` (required), `idCheckItem` (required).
Query params (all optional): `name`, `state`, `idChecklist`, `pos`, `due`, `dueReminder`, `idMember`.

```bash
scripts/trello.sh PUT "/cards/<id>/checkItem/<checkItemId>?name=My%20card"
```

## DELETE /cards/{id}/checkItem/{idCheckItem} — Delete checkItem on a Card
Path params: `id` (required), `idCheckItem` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/checkItem/<checkItemId>"
```

## GET /cards/{id}/checkItemStates — Get checkItems on a Card
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/checkItemStates?fields=name,desc"
```

## GET /cards/{id}/checklists — Get Checklists on a Card
Path params: `id` (required).
Query params (all optional): `checkItems`, `checkItem_fields`, `filter`, `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/checklists?checkItems=all"
```

## POST /cards/{id}/checklists — Create Checklist on a Card
Path params: `id` (required).
Query params (all optional): `name`, `idChecklistSource`, `pos`.

```bash
scripts/trello.sh POST "/cards/<id>/checklists?name=My%20card"
```

## DELETE /cards/{id}/checklists/{idChecklist} — Delete a Checklist on a Card
Path params: `id` (required), `idChecklist` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/checklists/<checklistId>"
```

## GET /cards/{id}/customFieldItems — Get Custom Field Items for a Card
Path params: `id` (required).

```bash
scripts/trello.sh GET "/cards/<id>/customFieldItems"
```

## POST /cards/{id}/idLabels — Add a Label to a Card
Path params: `id` (required).
Query params (all optional): `value`.

```bash
scripts/trello.sh POST "/cards/<id>/idLabels?value=<labelId>"
```

## DELETE /cards/{id}/idLabels/{idLabel} — Remove a Label from a Card
Path params: `id` (required), `idLabel` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/idLabels/<labelId>"
```

## POST /cards/{id}/idMembers — Add a Member to a Card
Path params: `id` (required).
Query params (all optional): `value`.

```bash
scripts/trello.sh POST "/cards/<id>/idMembers?value=<memberId>"
```

## DELETE /cards/{id}/idMembers/{idMember} — Remove a Member from a Card
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/idMembers/<memberId>"
```

## POST /cards/{id}/labels — Create a new Label on a Card
Path params: `id` (required).
Query params: `color` (required), `name`.

```bash
scripts/trello.sh POST "/cards/<id>/labels?color=red"
```

## GET /cards/{id}/list — Get the List of a Card
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/list?fields=name,desc"
```

## POST /cards/{id}/markAssociatedNotificationsRead — Mark a Card's Notifications as read
Path params: `id` (required).

```bash
scripts/trello.sh POST "/cards/<id>/markAssociatedNotificationsRead"
```

## GET /cards/{id}/members — Get the Members of a Card
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/members?fields=name,desc"
```

## GET /cards/{id}/membersVoted — Get Members who have voted on a Card
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/membersVoted?fields=name,desc"
```

## POST /cards/{id}/membersVoted — Add Member vote to Card
Path params: `id` (required).
Query params: `value` (required).

```bash
scripts/trello.sh POST "/cards/<id>/membersVoted?value=<memberId>"
```

## DELETE /cards/{id}/membersVoted/{idMember} — Remove a Member's Vote on a Card
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/membersVoted/<memberId>"
```

## GET /cards/{id}/pluginData — Get pluginData on a Card
Path params: `id` (required).

```bash
scripts/trello.sh GET "/cards/<id>/pluginData"
```

## GET /cards/{id}/stickers — Get Stickers on a Card
Path params: `id` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/stickers?fields=name,desc"
```

## POST /cards/{id}/stickers — Add a Sticker to a Card
Path params: `id` (required).
Query params: `image` (required), `top` (required), `left` (required), `zIndex` (required), `rotate`.

```bash
scripts/trello.sh POST "/cards/<id>/stickers?image=https%3A%2F%2Fexample.com%2Fimg.png&top=10&left=20&zIndex=1"
```

## GET /cards/{id}/stickers/{idSticker} — Get a Sticker on a Card
Path params: `id` (required), `idSticker` (required).
Query params (all optional): `fields`.

```bash
scripts/trello.sh GET "/cards/<id>/stickers/<stickerId>?fields=name,desc"
```

## PUT /cards/{id}/stickers/{idSticker} — Update a Sticker on a Card
Path params: `id` (required), `idSticker` (required).
Query params: `top` (required), `left` (required), `zIndex` (required), `rotate`.

```bash
scripts/trello.sh PUT "/cards/<id>/stickers/<stickerId>?top=10&left=20&zIndex=1"
```

## DELETE /cards/{id}/stickers/{idSticker} — Delete a Sticker on a Card
Path params: `id` (required), `idSticker` (required).

```bash
scripts/trello.sh DELETE "/cards/<id>/stickers/<stickerId>"
```

## GET /cards/{id}/{field} — Get a field on a Card
Path params: `id` (required), `field` (required).
Path `field`: name, desc, closed, dueComplete, dateLastActivity, idList, idBoard, pos, etc.

```bash
scripts/trello.sh GET "/cards/<id>/<field>"
```
