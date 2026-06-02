# Trello API — Search

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Search queries boards, cards, organizations, and
members visible to the token.

## GET /search — Search Trello
Query params: `query` (required). Optional: `idBoards`, `idOrganizations`, `idCards`, `modelTypes`, `board_fields`, `boards_limit`, `board_organization`, `card_fields`, `cards_limit`, `cards_page`, `card_board`, `card_list`, `card_members`, `card_stickers`, `card_attachments`, `organization_fields`, `organizations_limit`, `member_fields`, `members_limit`, `partial`.

```bash
scripts/trello.sh GET "/search?query=deploy&idBoards=<boardId>&modelTypes=cards"
```

## GET /search/members/ — Search for Members
Query params: `query` (required). Optional: `limit`, `idBoard`, `idOrganization`, `onlyOrgMembers`.

```bash
scripts/trello.sh GET "/search/members/?query=alice&limit=10"
```
