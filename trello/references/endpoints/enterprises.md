# Trello API — Enterprises

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Enterprises are paid accounts that govern
multiple Workspaces (Organizations) and their members.

## GET /enterprises/{id} — Get an Enterprise
Path params: `id` (required). Query params (all optional): `fields`, `members`, `member_fields`, `member_filter`, `member_sort`, `member_sortBy`, `member_sortOrder`, `member_startIndex`, `member_count`, `organizations`, `organization_fields`, `organization_paid_accounts`, `organization_memberships`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>?fields=name,displayName"
```

## GET /enterprises/{id}/auditlog — Get auditlog data for an Enterprise
Path params: `id` (required).

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/auditlog"
```

## GET /enterprises/{id}/admins — Get Enterprise admin Members
Path params: `id` (required). Query params: `fields` (optional).

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/admins?fields=fullName,username"
```

## GET /enterprises/{id}/signupUrl — Get signupUrl for Enterprise
Path params: `id` (required). Query params (all optional): `authenticate`, `confirmationAccepted`, `returnUrl`, `tosAccepted`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/signupUrl?returnUrl=https%3A%2F%2Fexample.com%2Fdone"
```

## GET /enterprises/{id}/members/query — Get Users of an Enterprise
Path params: `id` (required). Query params (all optional): `licensed`, `deactivated`, `collaborator`, `managed`, `admin`, `activeSince`, `inactiveSince`, `search`, `cursor`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/members/query?search=jane&licensed=true"
```

## GET /enterprises/{id}/members — Get Members of Enterprise
Path params: `id` (required). Query params (all optional): `fields`, `filter`, `sort`, `sortBy`, `sortOrder`, `startIndex`, `count`, `organization_fields`, `board_fields`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/members?count=50&startIndex=0"
```

## GET /enterprises/{id}/members/{idMember} — Get a Member of Enterprise
Path params: `id` (required), `idMember` (required). Query params (all optional): `fields`, `organization_fields`, `board_fields`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/members/<idMember>"
```

## GET /enterprises/{id}/transferrable/organization/{idOrganization} — Get whether an organization can be transferred to an enterprise.
Path params: `id` (required), `idOrganization` (required).

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/transferrable/organization/<orgId>"
```

## GET /enterprises/{id}/transferrable/bulk/{idOrganizations} — Get a bulk list of organizations that can be transferred to an enterprise.
Path params: `id` (required), `idOrganizations` (required).

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/transferrable/bulk/<orgId1>,<orgId2>"
```

## PUT /enterprises/{id}/enterpriseJoinRequest/bulk — Decline enterpriseJoinRequests from one organization or a bulk list of organizations.
Path params: `id` (required). Query params: `idOrganizations` (required).

```bash
scripts/trello.sh PUT "/enterprises/<enterpriseId>/enterpriseJoinRequest/bulk?idOrganizations=<orgId>"
```

## GET /enterprises/{id}/claimableOrganizations — Get ClaimableOrganizations of an Enterprise
Path params: `id` (required). Query params (all optional): `limit`, `cursor`, `name`, `activeSince`, `inactiveSince`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/claimableOrganizations?limit=100"
```

## GET /enterprises/{id}/pendingOrganizations — Get PendingOrganizations of an Enterprise
Path params: `id` (required). Query params (all optional): `activeSince`, `inactiveSince`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/pendingOrganizations"
```

## POST /enterprises/{id}/tokens — Create an auth Token for an Enterprise.
Path params: `id` (required). Query params: `expiration` (optional).

```bash
scripts/trello.sh POST "/enterprises/<enterpriseId>/tokens?expiration=30days"
```

## GET /enterprises/{id}/organizations — Get Organizations of an Enterprise
Path params: `id` (required). Query params (all optional): `fields`, `filter`, `startIndex`, `count`.

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/organizations?count=50"
```

## PUT /enterprises/{id}/organizations — Transfer an Organization to an Enterprise.
Path params: `id` (required). Query params: `idOrganization` (required).

```bash
scripts/trello.sh PUT "/enterprises/<enterpriseId>/organizations?idOrganization=<orgId>"
```

## PUT /enterprises/{id}/members/{idMember}/licensed — Update a Member's licensed status
Path params: `id` (required), `idMember` (required). Query params: `value` (required).

```bash
scripts/trello.sh PUT "/enterprises/<enterpriseId>/members/<idMember>/licensed?value=true"
```

## PUT /enterprises/{id}/members/{idMember}/deactivated — Deactivate a Member of an Enterprise.
Path params: `id` (required), `idMember` (required). Query params: `value` (required); optional: `fields`, `organization_fields`, `board_fields`.

```bash
scripts/trello.sh PUT "/enterprises/<enterpriseId>/members/<idMember>/deactivated?value=true"
```

## PUT /enterprises/{id}/admins/{idMember} — Update Member to be admin of Enterprise
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh PUT "/enterprises/<enterpriseId>/admins/<idMember>"
```

## DELETE /enterprises/{id}/admins/{idMember} — Remove a Member as admin from Enterprise.
Path params: `id` (required), `idMember` (required).

```bash
scripts/trello.sh DELETE "/enterprises/<enterpriseId>/admins/<idMember>"
```

## DELETE /enterprises/{id}/organizations/{idOrg} — Delete an Organization from an Enterprise.
Path params: `id` (required), `idOrg` (required).

```bash
scripts/trello.sh DELETE "/enterprises/<enterpriseId>/organizations/<orgId>"
```

## GET /enterprises/{id}/organizations/bulk/{idOrganizations} — Bulk accept a set of organizations to an Enterprise.
Path params: `id` (required), `idOrganizations` (required).

```bash
scripts/trello.sh GET "/enterprises/<enterpriseId>/organizations/bulk/<orgId1>,<orgId2>"
```
