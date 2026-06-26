# skills

Agent Skills for coding agents (Cursor, Claude Code, Codex, OpenCode, and more). Install with the [`skills` CLI](https://github.com/vercel-labs/skills).

## Skills

| Skill | Description |
|---|---|
| [`business-doc`](./business-doc) | Business documentation from a codebase: features, Mermaid flows, glossary, rules, KPIs, integrations, compliance. Optional `--frs` mode for requirements (RF/RNF). |
| [`commit`](./commit) | Plans and executes atomic Conventional Commits in dependency order (1–3 files each). Supports `/commit` with `--yes`, `--dry-run`, `--push`, and `--language` for splitting changes and writing commit messages. |
| [`django-superpowers`](./django-superpowers) | Django 5.0+ development: models, views, forms, URLs, admin, auth, security, testing, async, version features (5.0–6.0), plus DRF, SimpleJWT, django-allauth, django-environ, Celery, and Channels. |
| [`django-unfold`](./django-unfold) | Django Unfold admin theme: install, UNFOLD settings, ModelAdmin, filters, actions, tabs, inlines, widgets, dashboards, third-party integrations, and troubleshooting. |
| [`security-check`](./security-check) | Security review of code, APIs, infrastructure, or architecture against OWASP Top 10, CWE Top 25, and secure coding practices. DREAD/CVSS severity, remediation guidance — language and framework agnostic. Covers injection, auth, JWT/OAuth, GraphQL, cloud/IaC, and threat modeling. |
| [`trello`](./trello) | Trello REST API (boards, lists, cards, checklists, members, labels, webhooks, and more) via `curl` / PowerShell wrappers and env-based credentials. |

## Installation

```bash
npx skills add silasvasconcelos/skills --skill trello
```

Replace `trello` with any skill name from the table above.

### Useful options (`skills add`)

| Option | Description |
|---|---|
| `-s, --skill <name>` | Install only the named skill(s). Use `'*'` for all. Repeatable. |
| `-a, --agent <name>` | Install only to selected agents (e.g. `cursor`, `claude-code`, `codex`). Repeatable. Use `'*'` for all. |
| `-g, --global` | Install to the user directory (`~/…/skills/`), available across projects. Default: project scope (`./…/skills/`). |
| `-l, --list` | List skills in the repository without installing. |
| `--all` | Install all skills to all agents without prompts. |
| `--copy` | Copy files instead of symlinking (when symlinks are not supported). |
| `-y, --yes` | Skip confirmation prompts (CI/CD friendly). |

Full CLI reference: [vercel-labs/skills](https://github.com/vercel-labs/skills).

### Examples

```bash
# List skills available in this repository
npx skills add silasvasconcelos/skills --list

# Install to Cursor only
npx skills add silasvasconcelos/skills --skill business-doc -a cursor

# Multiple skills and agents
npx skills add silasvasconcelos/skills -s business-doc -s trello -a cursor -a claude-code

# Global install, no prompts
npx skills add silasvasconcelos/skills --skill trello -g -y

# All skills from this repo
npx skills add silasvasconcelos/skills --all
```

### Other commands

| Command | Description |
|---|---|
| `npx skills list` | List installed skills (`ls`). `-g` for global only; `-a <agent>` to filter by agent. |
| `npx skills update` | Update installed skills. `-g` / `-p` limit scope; `-y` skips prompts. |
| `npx skills remove <name>` | Remove a skill (`rm`). `-a`, `-g`, `--all` work like `add`. |
| `npx skills find [query]` | Search the skills ecosystem ([skills.sh](https://skills.sh)). |
