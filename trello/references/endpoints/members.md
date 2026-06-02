# Trello API — Members

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Use `me` as `{id}` for the authenticated member.

## GET /members/{id} — Get a Member
Path params: `id` (required).
Query params: `actions` (optional), `boards` (optional), `boardBackgrounds` (optional), `boardsInvited` (optional), `boardsInvited_fields` (optional), `boardStars` (optional), `cards` (optional), `customBoardBackgrounds` (optional), `customEmoji` (optional), `customStickers` (optional), `fields` (optional), `notifications` (optional), `organizations` (optional), `organization_fields` (optional), `organization_paid_account` (optional), `organizationsInvited` (optional), `organizationsInvited_fields` (optional), `paid_account` (optional), `savedSearches` (optional), `tokens` (optional).

```bash
scripts/trello.sh GET "/members/me"
```

## PUT /members/{id} — Update a Member
Path params: `id` (required).
Query params: `fullName` (optional), `initials` (optional), `username` (optional), `bio` (optional), `avatarSource` (optional), `prefs/colorBlind` (optional), `prefs/locale` (optional), `prefs/minutesBetweenSummaries` (optional).

```bash
scripts/trello.sh PUT "/members/me"
```

## GET /members/{id}/actions — Get a Member's Actions
Path params: `id` (required).
Query params: `filter` (optional).

```bash
scripts/trello.sh GET "/members/me/actions"
```

## POST /members/{id}/avatar — Create Avatar for Member
Path params: `id` (required).
Query params: `file` (required).

```bash
scripts/trello.sh POST "/members/me/avatar?file=@/path/to/image.png"
```

## GET /members/{id}/boardBackgrounds — Get Member's custom Board backgrounds
Path params: `id` (required).
Query params: `filter` (optional).

```bash
scripts/trello.sh GET "/members/me/boardBackgrounds"
```

## POST /members/{id}/boardBackgrounds — Upload new boardBackground for Member
Path params: `id` (required).
Query params: `file` (required).

```bash
scripts/trello.sh POST "/members/me/boardBackgrounds?file=@/path/to/image.png"
```

## DELETE /members/{id}/boardBackgrounds/{idBackground} — Delete a Member's custom Board background
Path params: `id` (required), `idBackground` (required).

```bash
scripts/trello.sh DELETE "/members/me/boardBackgrounds/<idBackground>"
```

## GET /members/{id}/boardBackgrounds/{idBackground} — Get a boardBackground of a Member
Path params: `id` (required), `idBackground` (required).
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/members/me/boardBackgrounds/<idBackground>"
```

## PUT /members/{id}/boardBackgrounds/{idBackground} — Update a Member's custom Board background
Path params: `id` (required), `idBackground` (required).
Query params: `brightness` (optional), `tile` (optional).

```bash
scripts/trello.sh PUT "/members/me/boardBackgrounds/<idBackground>"
```

## GET /members/{id}/boardStars — Get a Member's boardStars
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/boardStars"
```

## POST /members/{id}/boardStars — Create Star for Board
Path params: `id` (required).
Query params: `idBoard` (required), `pos` (required).

```bash
scripts/trello.sh POST "/members/me/boardStars?idBoard=<boardId>&pos=top"
```

## DELETE /members/{id}/boardStars/{idStar} — Delete Star for Board
Path params: `id` (required), `idStar` (required).

```bash
scripts/trello.sh DELETE "/members/me/boardStars/<idStar>"
```

## GET /members/{id}/boardStars/{idStar} — Get a boardStar of Member
Path params: `id` (required), `idStar` (required).

```bash
scripts/trello.sh GET "/members/me/boardStars/<idStar>"
```

## PUT /members/{id}/boardStars/{idStar} — Update the position of a boardStar of Member
Path params: `id` (required), `idStar` (required).
Query params: `pos` (optional).

```bash
scripts/trello.sh PUT "/members/me/boardStars/<idStar>"
```

## GET /members/{id}/boards — Get Boards that Member belongs to
Path params: `id` (required).
Query params: `filter` (optional), `fields` (optional), `lists` (optional), `organization` (optional), `organization_fields` (optional).

```bash
scripts/trello.sh GET "/members/me/boards"
```

## GET /members/{id}/boardsInvited — Get Boards the Member has been invited to
Path params: `id` (required).
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/members/me/boardsInvited"
```

## GET /members/{id}/cards — Get Cards the Member is on
Path params: `id` (required).
Query params: `filter` (optional).

```bash
scripts/trello.sh GET "/members/me/cards"
```

## GET /members/{id}/customBoardBackgrounds — Get a Member's custom Board Backgrounds
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/customBoardBackgrounds"
```

## POST /members/{id}/customBoardBackgrounds — Create a new custom Board Background
Path params: `id` (required).
Query params: `file` (required).

```bash
scripts/trello.sh POST "/members/me/customBoardBackgrounds?file=@/path/to/image.png"
```

## DELETE /members/{id}/customBoardBackgrounds/{idBackground} — Delete custom Board Background of Member
Path params: `id` (required), `idBackground` (required).

```bash
scripts/trello.sh DELETE "/members/me/customBoardBackgrounds/<idBackground>"
```

## GET /members/{id}/customBoardBackgrounds/{idBackground} — Get custom Board Background of Member
Path params: `id` (required), `idBackground` (required).

```bash
scripts/trello.sh GET "/members/me/customBoardBackgrounds/<idBackground>"
```

## PUT /members/{id}/customBoardBackgrounds/{idBackground} — Update custom Board Background of Member
Path params: `id` (required), `idBackground` (required).
Query params: `brightness` (optional), `tile` (optional).

```bash
scripts/trello.sh PUT "/members/me/customBoardBackgrounds/<idBackground>"
```

## GET /members/{id}/customEmoji — Get a Member's customEmojis
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/customEmoji"
```

## POST /members/{id}/customEmoji — Create custom Emoji for Member
Path params: `id` (required).
Query params: `file` (required), `name` (required).

```bash
scripts/trello.sh POST "/members/me/customEmoji?file=@/path/to/image.png&name=My%20emoji"
```

## GET /members/{id}/customEmoji/{idEmoji} — Get a Member's custom Emoji
Path params: `id` (required), `idEmoji` (required).
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/members/me/customEmoji/<idEmoji>"
```

## GET /members/{id}/customStickers — Get Member's custom Stickers
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/customStickers"
```

## POST /members/{id}/customStickers — Create custom Sticker for Member
Path params: `id` (required).
Query params: `file` (required).

```bash
scripts/trello.sh POST "/members/me/customStickers?file=@/path/to/image.png"
```

## DELETE /members/{id}/customStickers/{idSticker} — Delete a Member's custom Sticker
Path params: `id` (required), `idSticker` (required).

```bash
scripts/trello.sh DELETE "/members/me/customStickers/<idSticker>"
```

## GET /members/{id}/customStickers/{idSticker} — Get a Member's custom Sticker
Path params: `id` (required), `idSticker` (required).
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/members/me/customStickers/<idSticker>"
```

## GET /members/{id}/notifications — Get Member's Notifications
Path params: `id` (required).
Query params: `entities` (optional), `display` (optional), `filter` (optional), `read_filter` (optional), `fields` (optional), `limit` (optional), `page` (optional), `before` (optional), `since` (optional), `memberCreator` (optional), `memberCreator_fields` (optional).

```bash
scripts/trello.sh GET "/members/me/notifications"
```

## GET /members/{id}/notificationsChannelSettings — Get a Member's notification channel settings
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/notificationsChannelSettings"
```

## PUT /members/{id}/notificationsChannelSettings — Update blocked notification keys of Member on a channel
Path params: `id` (required).
JSON body: `channel` (required), `blockedKeys` (required).

```bash
scripts/trello.sh PUT "/members/me/notificationsChannelSettings" --data '{"channel":"email","blockedKeys":"cardDueSoon"}'
```

## GET /members/{id}/notificationsChannelSettings/{channel} — Get blocked notification keys of Member on this channel
Path params: `id` (required), `channel` (required).

```bash
scripts/trello.sh GET "/members/me/notificationsChannelSettings/email"
```

## PUT /members/{id}/notificationsChannelSettings/{channel} — Update blocked notification keys of Member on a channel
Path params: `id` (required), `channel` (required).
JSON body: `blockedKeys` (required).

```bash
scripts/trello.sh PUT "/members/me/notificationsChannelSettings/email" --data '{"blockedKeys":"cardDueSoon"}'
```

## PUT /members/{id}/notificationsChannelSettings/{channel}/{blockedKeys} — Update blocked notification keys of Member on a channel
Path params: `id` (required), `channel` (required), `blockedKeys` (required).

```bash
scripts/trello.sh PUT "/members/me/notificationsChannelSettings/email/<blockedKeys>"
```

## POST /members/{id}/oneTimeMessagesDismissed — Dismiss a message for Member
Path params: `id` (required).
Query params: `value` (required).

```bash
scripts/trello.sh POST "/members/me/oneTimeMessagesDismissed?value=<messageKey>"
```

## GET /members/{id}/organizations — Get Member's Organizations
Path params: `id` (required).
Query params: `filter` (optional), `fields` (optional), `paid_account` (optional).

```bash
scripts/trello.sh GET "/members/me/organizations"
```

## GET /members/{id}/organizationsInvited — Get Organizations a Member has been invited to
Path params: `id` (required).
Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/members/me/organizationsInvited"
```

## GET /members/{id}/savedSearches — Get Member's saved searched
Path params: `id` (required).

```bash
scripts/trello.sh GET "/members/me/savedSearches"
```

## POST /members/{id}/savedSearches — Create saved Search for Member
Path params: `id` (required).
Query params: `name` (required), `query` (required), `pos` (required).

```bash
scripts/trello.sh POST "/members/me/savedSearches?name=Open%20cards&query=is:open&pos=top"
```

## DELETE /members/{id}/savedSearches/{idSearch} — Delete a saved search
Path params: `id` (required), `idSearch` (required).

```bash
scripts/trello.sh DELETE "/members/me/savedSearches/<idSearch>"
```

## GET /members/{id}/savedSearches/{idSearch} — Get a saved search
Path params: `id` (required), `idSearch` (required).

```bash
scripts/trello.sh GET "/members/me/savedSearches/<idSearch>"
```

## PUT /members/{id}/savedSearches/{idSearch} — Update a saved search
Path params: `id` (required), `idSearch` (required).
Query params: `name` (optional), `query` (optional), `pos` (optional).

```bash
scripts/trello.sh PUT "/members/me/savedSearches/<idSearch>"
```

## GET /members/{id}/tokens — Get Member's Tokens
Path params: `id` (required).
Query params: `webhooks` (optional).

```bash
scripts/trello.sh GET "/members/me/tokens"
```

## GET /members/{id}/{field} — Get a field on a Member
Path params: `id` (required), `field` (required). Path `field` is a Member
field name (e.g. `username`, `fullName`, `bio`, `url`).

```bash
scripts/trello.sh GET "/members/me/username"
```

