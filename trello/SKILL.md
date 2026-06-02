---
name: trello
description: Call the Trello REST API (boards, lists, cards, checklists, members, labels, webhooks, organizations, enterprises, and more) using curl on macOS/Linux or PowerShell on Windows. Reads credentials from environment variables. Use when the user wants to read or modify Trello data, automate Trello, or mentions Trello boards, cards, lists, or the Trello API.
---

# Trello

Cross-platform client for the **Trello REST API** (`https://api.trello.com/1`).
It covers every endpoint in the official spec, grouped by resource, and runs the
same way on macOS, Linux, and Windows.

## Prerequisites: credentials

All requests authenticate with two values pulled from environment variables:

- `TRELLO_API_KEY` — your app/Power-Up key (public-safe).
- `TRELLO_API_TOKEN` — grants access to the user's account (**secret**). `TRELLO_TOKEN` works as a fallback.

If either is missing, **stop and walk the user through obtaining and exporting
them** using [references/authentication.md](references/authentication.md). Do not
ask the user to paste secrets into the chat; have them export the variables.

## Prerequisites: HTTP client

| OS | Client | Wrapper script |
|---|---|---|
| macOS / Linux (and Git Bash / WSL) | `curl` | `scripts/trello.sh` |
| Windows | `Invoke-RestMethod` (built into PowerShell) | `scripts/trello.ps1` |

Choose the script matching the user's OS. If `curl` is missing on macOS/Linux,
run `scripts/ensure-curl.sh` to install it. On Windows, `Invoke-RestMethod` is
built in; `scripts/ensure-curl.ps1` verifies the environment and can optionally
install `curl.exe`.

## How to call any endpoint

Both wrappers take a method and a path (with optional query string) and append
`key`/`token` automatically — never put credentials in the path.

```bash
# macOS / Linux
scripts/trello.sh <METHOD> "<PATH[?query]>" [--data '<json>']
```

```powershell
# Windows
./scripts/trello.ps1 <METHOD> "<PATH[?query]>" [-Data '<json>']
```

### Examples

```bash
# List your boards (names + URLs only)
scripts/trello.sh GET "/members/me/boards?fields=name,url"

# Create a card on a list
scripts/trello.sh POST "/cards?idList=<listId>&name=New%20card"

# Rename a card via JSON body
scripts/trello.sh PUT "/cards/<cardId>" --data '{"name":"Renamed"}'

# Delete a card
scripts/trello.sh DELETE "/cards/<cardId>"
```

```powershell
./scripts/trello.ps1 GET "/members/me/boards?fields=name,url"
./scripts/trello.ps1 POST "/cards?idList=<listId>&name=New card"
./scripts/trello.ps1 PUT "/cards/<cardId>" -Data '{"name":"Renamed"}'
```

> Query-string params and JSON bodies are both supported. When passing a body,
> the wrapper sets `Content-Type: application/json`. URL-encode spaces/special
> characters in query values (`%20` for space) when using the path query string.

## Finding the right endpoint

Endpoints are documented one file per resource group under
[references/endpoints/](references/endpoints/). Read only the group you need:

| Resource | Reference |
|---|---|
| Actions (audit log, comments) | [actions.md](references/endpoints/actions.md) |
| Applications | [applications.md](references/endpoints/applications.md) |
| Batch requests | [batch.md](references/endpoints/batch.md) |
| Boards | [boards.md](references/endpoints/boards.md) |
| Cards | [cards.md](references/endpoints/cards.md) |
| Checklists | [checklists.md](references/endpoints/checklists.md) |
| Custom Fields | [customfields.md](references/endpoints/customfields.md) |
| Emoji | [emoji.md](references/endpoints/emoji.md) |
| Enterprises | [enterprises.md](references/endpoints/enterprises.md) |
| Labels | [labels.md](references/endpoints/labels.md) |
| Lists | [lists.md](references/endpoints/lists.md) |
| Members | [members.md](references/endpoints/members.md) |
| Notifications | [notifications.md](references/endpoints/notifications.md) |
| Organizations (Workspaces) | [organizations.md](references/endpoints/organizations.md) |
| Plugins (Power-Ups) | [plugins.md](references/endpoints/plugins.md) |
| Search | [search.md](references/endpoints/search.md) |
| Tokens | [tokens.md](references/endpoints/tokens.md) |
| Webhooks | [webhooks.md](references/endpoints/webhooks.md) |

The full machine-readable spec is `references/trello-openapi.json` if you need
exact parameter names or schemas beyond the per-group docs.

## Workflow

1. Confirm `TRELLO_API_KEY` and `TRELLO_API_TOKEN` are set; if not, follow [authentication.md](references/authentication.md).
2. Confirm the HTTP client is available (install via the `ensure-curl` script if needed).
3. Identify the resource group and open its reference file for the exact path/params.
4. Call the endpoint with the OS-appropriate wrapper script.
5. On `401` re-check credentials; on `429` you hit a rate limit — back off and retry.

## Notes & gotchas

- IDs: most paths accept a 24-char object ID; cards/boards also accept their shortlink.
- `me` is a shortcut for the authenticated member (e.g. `/members/me`).
- List endpoints cap at 1000 results; page with `before`/`since` (see actions.md).
- Prefer webhooks over polling for change notifications (see webhooks.md).
