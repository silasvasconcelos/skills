# Trello API — Boards

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Boards are the top-level container for lists,
cards, labels, and members.

## POST /boards/ — Create a Board
Query params: `name` (required), `defaultLabels`, `defaultLists`, `desc`, `idOrganization`, `idBoardSource`, `keepFromSource`, `powerUps`, `prefs_permissionLevel`, `prefs_voting`, `prefs_comments`, `prefs_invitations`, `prefs_selfJoin`, `prefs_cardCovers`, `prefs_background`, `prefs_cardAging` (all optional except `name`).

```bash
scripts/trello.sh POST "/boards/?name=My%20Board&defaultLists=true"
```

## GET /boards/{id} — Get a Board
Path params: `id` (required). Query params (all optional): `actions`, `boardStars`, `cards`, `card_pluginData`, `checklists`, `customFields`, `fields`, `labels`, `lists`, `members`, `memberships`, `pluginData`, `organization`, `organization_pluginData`, `myPrefs`, `tags`.

```bash
scripts/trello.sh GET "/boards/<id>?fields=name,url,desc&lists=open"
```

## PUT /boards/{id} — Update a Board
Path params: `id` (required). Query params (all optional): `name`, `desc`, `closed`, `subscribed`, `idOrganization`, `prefs/permissionLevel`, `prefs/selfJoin`, `prefs/cardCovers`, `prefs/hideVotes`, `prefs/invitations`, `prefs/voting`, `prefs/comments`, `prefs/background`, `prefs/cardAging`, `prefs/calendarFeedEnabled`.

```bash
scripts/trello.sh PUT "/boards/<id>?name=Renamed%20Board&closed=false"
```

## DELETE /boards/{id} — Delete a Board
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/boards/<id>"
```

## GET /boards/{id}/{field} — Get a field on a Board
Path params: `id` (required), `field` (required; one of `closed`, `dateLastActivity`, `dateLastView`, `desc`, `descData`, `idMemberCreator`, `idOrganization`, `invitations`, `invited`, `labelNames`, `memberships`, `name`, `pinned`, `powerUps`, `prefs`, `shortLink`, `shortUrl`, `starred`, `subscribed`, `url`).

```bash
scripts/trello.sh GET "/boards/<id>/name"
```

## GET /boards/{boardId}/actions — Get Actions of a Board
Path params: `boardId` (required). Query params (all optional): `fields`, `filter`, `format`, `idModels`, `limit`, `member`, `member_fields`, `memberCreator`, `memberCreator_fields`, `page`, `reactions`, `before`, `since`.

```bash
scripts/trello.sh GET "/boards/<boardId>/actions?limit=50&filter=createCard,updateCard"
```

## GET /boards/{boardId}/boardStars — Get boardStars on a Board
Path params: `boardId` (required). Query params: `filter` (optional; `mine` or `none`).

```bash
scripts/trello.sh GET "/boards/<boardId>/boardStars?filter=mine"
```

## GET /boards/{id}/boardPlugins — Get Enabled Power-Ups on Board
Path params: `id` (required).

```bash
scripts/trello.sh GET "/boards/<id>/boardPlugins"
```

## POST /boards/{id}/boardPlugins — Enable a Power-Up on a Board
Path params: `id` (required). Query params: `idPlugin` (optional).

```bash
scripts/trello.sh POST "/boards/<id>/boardPlugins?idPlugin=<pluginId>"
```

## DELETE /boards/{id}/boardPlugins/{idPlugin} — Disable a Power-Up on a Board
Path params: `id` (required), `idPlugin` (required).

```bash
scripts/trello.sh DELETE "/boards/<id>/boardPlugins/<idPlugin>"
```

## POST /boards/{id}/calendarKey/generate — Create a calendarKey for a Board
Path params: `id` (required).

```bash
scripts/trello.sh POST "/boards/<id>/calendarKey/generate"
```

## GET /boards/{id}/cards — Get Cards on a Board
Path params: `id` (required).

```bash
scripts/trello.sh GET "/boards/<id>/cards"
```

## GET /boards/{id}/cards/{filter} — Get filtered Cards on a Board
Path params: `id` (required), `filter` (required; one of `all`, `closed`, `complete`, `incomplete`, `none`, `open`, `visible`).

```bash
scripts/trello.sh GET "/boards/<id>/cards/open"
```

## GET /boards/{id}/checklists — Get Checklists on a Board
Path params: `id` (required).

```bash
scripts/trello.sh GET "/boards/<id>/checklists"
```

## GET /boards/{id}/customFields — Get Custom Fields for Board
Path params: `id` (required).

```bash
scripts/trello.sh GET "/boards/<id>/customFields"
```

## POST /boards/{id}/emailKey/generate — Create a emailKey for a Board
Path params: `id` (required).

```bash
scripts/trello.sh POST "/boards/<id>/emailKey/generate"
```

## POST /boards/{id}/idTags — Create a Tag for a Board
Path params: `id` (required). Query params: `value` (required; organization tag id).

```bash
scripts/trello.sh POST "/boards/<id>/idTags?value=<tagId>"
```

## GET /boards/{id}/labels — Get Labels on a Board
Path params: `id` (required). Query params (optional): `fields`, `limit`.

```bash
scripts/trello.sh GET "/boards/<id>/labels?limit=50"
```

## POST /boards/{id}/labels — Create a Label on a Board
Path params: `id` (required). Query params: `name` (required), `color` (required; label color or `null`).

```bash
scripts/trello.sh POST "/boards/<id>/labels?name=Bug&color=red"
```

## GET /boards/{id}/lists — Get Lists on a Board
Path params: `id` (required). Query params (all optional): `cards`, `card_fields`, `filter`, `fields`.

```bash
scripts/trello.sh GET "/boards/<id>/lists?filter=open&fields=name,pos"
```

## POST /boards/{id}/lists — Create a List on a Board
Path params: `id` (required). Query params: `name` (required), `pos` (optional; `top`, `bottom`, or positive number).

```bash
scripts/trello.sh POST "/boards/<id>/lists?name=To%20Do&pos=top"
```

## GET /boards/{id}/lists/{filter} — Get filtered Lists on a Board
Path params: `id` (required), `filter` (required; one of `all`, `closed`, `none`, `open`).

```bash
scripts/trello.sh GET "/boards/<id>/lists/open"
```

## POST /boards/{id}/markedAsViewed — Mark Board as viewed
Path params: `id` (required).

```bash
scripts/trello.sh POST "/boards/<id>/markedAsViewed"
```

## GET /boards/{id}/members — Get the Members of a Board
Path params: `id` (required).

```bash
scripts/trello.sh GET "/boards/<id>/members"
```

## PUT /boards/{id}/members — Invite Member to Board via email
Path params: `id` (required). Query params: `email` (required), `type` (optional; `admin`, `normal`, `observer`). Request body (JSON, optional): `fullName`.

```bash
scripts/trello.sh PUT "/boards/<id>/members?email=user@example.com&type=normal"
```

## PUT /boards/{id}/members/{idMember} — Add a Member to a Board
Path params: `id` (required), `idMember` (required). Query params: `type` (required; `admin`, `normal`, `observer`), `allowBillableGuest` (optional).

```bash
scripts/trello.sh PUT "/boards/<id>/members/<idMember>?type=normal"
```

## DELETE /boards/{id}/members/{idMember} — Remove Member from Board
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/boards/<id>/members/<idMember>"
```

## GET /boards/{id}/memberships — Get Memberships of a Board
Path params: `id` (required). Query params (all optional): `filter`, `activity`, `orgMemberType`, `member`, `member_fields`.

```bash
scripts/trello.sh GET "/boards/<id>/memberships?filter=all&member=true"
```

## PUT /boards/{id}/memberships/{idMembership} — Update Membership of Member on a Board
Path params: `id` (required), `idMembership` (required). Query params: `type` (required; `admin`, `normal`, `observer`), `member_fields` (optional).

```bash
scripts/trello.sh PUT "/boards/<id>/memberships/<idMembership>?type=admin"
```

## PUT /boards/{id}/myPrefs/emailPosition — Update emailPosition Pref on a Board
Path params: `id` (required). Query params: `value` (required; `bottom` or `top`).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/emailPosition?value=top"
```

## PUT /boards/{id}/myPrefs/idEmailList — Update idEmailList Pref on a Board
Path params: `id` (required). Query params: `value` (required; email list id).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/idEmailList?value=<listId>"
```

## PUT /boards/{id}/myPrefs/showSidebar — Update showSidebar Pref on a Board
Path params: `id` (required). Query params: `value` (required; boolean).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/showSidebar?value=true"
```

## PUT /boards/{id}/myPrefs/showSidebarActivity — Update showSidebarActivity Pref on a Board
Path params: `id` (required). Query params: `value` (required; boolean).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/showSidebarActivity?value=true"
```

## PUT /boards/{id}/myPrefs/showSidebarBoardActions — Update showSidebarBoardActions Pref on a Board
Path params: `id` (required). Query params: `value` (required; boolean).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/showSidebarBoardActions?value=false"
```

## PUT /boards/{id}/myPrefs/showSidebarMembers — Update showSidebarMembers Pref on a Board
Path params: `id` (required). Query params: `value` (required; boolean).

```bash
scripts/trello.sh PUT "/boards/<id>/myPrefs/showSidebarMembers?value=true"
```

## GET /boards/{id}/plugins — Get Power-Ups on a Board
Path params: `id` (required). Query params: `filter` (optional; `enabled` or `available`).

```bash
scripts/trello.sh GET "/boards/<id>/plugins?filter=enabled"
```
