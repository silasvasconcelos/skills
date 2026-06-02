# Trello API — Organizations

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Organizations are also called Workspaces — the
container for boards and team membership.

## POST /organizations/ — Create a new Organization
Query params: `displayName` (required), `desc`, `name`, `website` (all optional except `displayName`).

```bash
scripts/trello.sh POST "/organizations/?displayName=My%20Workspace&desc=Team%20boards"
```

## GET /organizations/{id} — Get an Organization
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>"
```

## PUT /organizations/{id} — Update an Organization
Path params: `id` (required). Query params (all optional): `name`, `displayName`, `desc`, `website`, `prefs/associatedDomain`, `prefs/externalMembersDisabled`, `prefs/googleAppsVersion`, `prefs/boardVisibilityRestrict/org`, `prefs/boardVisibilityRestrict/private`, `prefs/boardVisibilityRestrict/public`, `prefs/orgInviteRestrict`, `prefs/permissionLevel`.

```bash
scripts/trello.sh PUT "/organizations/<orgId>?displayName=Renamed%20Workspace"
```

## DELETE /organizations/{id} — Delete an Organization
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>"
```

## GET /organizations/{id}/{field} — Get field on Organization
Path params: `id` (required), `field` (required; one of `id`, `name`).

```bash
scripts/trello.sh GET "/organizations/<orgId>/name"
```

## GET /organizations/{id}/actions — Get Actions for Organization
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/actions"
```

## GET /organizations/{id}/boards — Get Boards in an Organization
Path params: `id` (required). Query params: `filter`, `fields` (optional).

```bash
scripts/trello.sh GET "/organizations/<orgId>/boards?filter=open"
```

## POST /organizations/{id}/exports — Create Export for Organizations
Path params: `id` (required). Query params: `attachments` (optional).

```bash
scripts/trello.sh POST "/organizations/<orgId>/exports?attachments=true"
```

## GET /organizations/{id}/exports — Retrieve Organization's Exports
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/exports"
```

## GET /organizations/{id}/members — Get the Members of an Organization
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/members"
```

## PUT /organizations/{id}/members — Update an Organization's Members
Path params: `id` (required). Query params: `email` (required), `fullName` (required), `type` (optional).

```bash
scripts/trello.sh PUT "/organizations/<orgId>/members?email=user@example.com&fullName=Jane%20Doe&type=normal"
```

## GET /organizations/{id}/memberships — Get Memberships of an Organization
Path params: `id` (required). Query params: `filter`, `member` (optional).

```bash
scripts/trello.sh GET "/organizations/<orgId>/memberships?filter=active"
```

## GET /organizations/{id}/memberships/{idMembership} — Get a Membership of an Organization
Path params: `id` (required), `idMembership` (required). Query params: `member` (optional).

```bash
scripts/trello.sh GET "/organizations/<orgId>/memberships/<idMembership>"
```

## GET /organizations/{id}/pluginData — Get the pluginData Scoped to Organization
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/pluginData"
```

## GET /organizations/{id}/tags — Get Tags of an Organization
Path params: `id` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/tags"
```

## POST /organizations/{id}/tags — Create a Tag in Organization
Path params: `id` (required).

```bash
scripts/trello.sh POST "/organizations/<orgId>/tags"
```

## PUT /organizations/{id}/members/{idMember} — Update a Member of an Organization
Path params: `id` (required), `idMember` (required). Query params: `type` (required).

```bash
scripts/trello.sh PUT "/organizations/<orgId>/members/<idMember>?type=admin"
```

## DELETE /organizations/{id}/members/{idMember} — Remove a Member from an Organization
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/members/<idMember>"
```

## PUT /organizations/{id}/members/{idMember}/deactivated — Deactivate or reactivate a member of an Organization
Path params: `id` (required), `idMember` (required). Query params: `value` (required).

```bash
scripts/trello.sh PUT "/organizations/<orgId>/members/<idMember>/deactivated?value=true"
```

## POST /organizations/{id}/logo — Update logo for an Organization
Path params: `id` (required). Query params: `file` (optional).

```bash
scripts/trello.sh POST "/organizations/<orgId>/logo?file=@logo.png"
```

## DELETE /organizations/{id}/logo — Delete Logo for Organization
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/logo"
```

## DELETE /organizations/{id}/members/{idMember}/all — Remove a Member from an Organization and all Organization Boards
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/members/<idMember>/all"
```

## DELETE /organizations/{id}/prefs/associatedDomain — Remove the associated Google Apps domain from a Workspace
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/prefs/associatedDomain"
```

## DELETE /organizations/{id}/prefs/orgInviteRestrict — Delete the email domain restriction on who can be invited to the Workspace
Path params: `id` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/prefs/orgInviteRestrict"
```

## DELETE /organizations/{id}/tags/{idTag} — Delete an Organization's Tag
Path params: `id` (required), `idTag` (required).

```bash
scripts/trello.sh DELETE "/organizations/<orgId>/tags/<idTag>"
```

## GET /organizations/{id}/newBillableGuests/{idBoard} — Get Organizations new billable guests
Path params: `id` (required), `idBoard` (required).

```bash
scripts/trello.sh GET "/organizations/<orgId>/newBillableGuests/<idBoard>"
```
