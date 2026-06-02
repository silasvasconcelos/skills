# Trello authentication — get & set your API key and token

The skill reads two secrets from environment variables:

| Variable | Purpose | Public? |
|---|---|---|
| `TRELLO_API_KEY` | Identifies your app (Power-Up). | Public-safe. |
| `TRELLO_API_TOKEN` | Grants access to **your** Trello account. | **Secret — never commit or share.** |

`TRELLO_TOKEN` is accepted as a fallback name for the token.

> Source: Trello REST API — [API Introduction](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).

## Step 1 — Get the API key

1. You must first have a Trello **Power-Up**. Create one via the [Managing Apps](https://developer.atlassian.com/cloud/trello/guides/power-ups/managing-power-ups/) docs if you don't have one.
2. Open <https://trello.com/power-ups/admin>.
3. Select your Power-Up → **API Key** tab → **Generate a new API Key**.
4. Copy the key (a 32-char hex string).

## Step 2 — Get the API token

1. On the same **API Key** page, click the hyperlinked **Token** to the right of the key.
2. The authorization screen appears. Click **Allow** to grant your own app access to your account.
3. Copy the token shown on the redirect page.

> This token can read and write your entire Trello account. Keep it secret.

## Step 3 — Set the environment variables

### macOS / Linux (bash or zsh)

Temporary (current shell only):

```bash
export TRELLO_API_KEY="your_key_here"
export TRELLO_API_TOKEN="your_token_here"
```

Persistent — append to your shell profile, then reload:

```bash
# zsh (macOS default)
echo 'export TRELLO_API_KEY="your_key_here"'   >> ~/.zshrc
echo 'export TRELLO_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc

# bash
echo 'export TRELLO_API_KEY="your_key_here"'   >> ~/.bashrc
echo 'export TRELLO_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Windows — PowerShell

Temporary (current session only):

```powershell
$env:TRELLO_API_KEY   = "your_key_here"
$env:TRELLO_API_TOKEN = "your_token_here"
```

Persistent (current user, new sessions):

```powershell
setx TRELLO_API_KEY "your_key_here"
setx TRELLO_API_TOKEN "your_token_here"
# Close and reopen PowerShell for setx values to take effect.
```

### Windows — Command Prompt (cmd.exe)

```bat
set TRELLO_API_KEY=your_key_here
set TRELLO_API_TOKEN=your_token_here
:: Persist across sessions:
setx TRELLO_API_KEY "your_key_here"
setx TRELLO_API_TOKEN "your_token_here"
```

## Step 4 — Verify

```bash
# macOS / Linux
scripts/trello.sh GET "/members/me?fields=username,fullName"
```

```powershell
# Windows
./scripts/trello.ps1 GET "/members/me?fields=username,fullName"
```

A JSON object with your username confirms the credentials work. A `401`
means the key/token is missing, wrong, or revoked.
