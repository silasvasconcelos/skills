# skills

A collection of open-source [Agent Skills](https://github.com/vercel-labs/skills) for AI coding agents (Cursor, Claude Code, Codex, OpenCode, and more).

Each skill lives in its own top-level folder with a `SKILL.md` entry point and optional `templates/`. Install one, several, or all of them with the `skills` CLI.

## Skills

| Skill | Description |
|---|---|
| [`business-doc`](./business-doc) | Generates business (non-technical) documentation from an existing codebase. Organizes by feature/user story with Mermaid flows, glossary, business rules, KPIs, integrations, compliance, and open questions. Supports parallel subagents and an `--frs` mode for Software Requirements (RF/RNF) docs. |

## Installation

Skills are installed with the [`skills` CLI](https://www.npmjs.com/package/skills) via `npx`. No global install required.

### Install everything

```bash
npx skills add silasvasconcelos/skills
```

### Install a specific skill

```bash
npx skills add silasvasconcelos/skills --skill business-doc
```

### Target specific agents

```bash
# e.g. Cursor + Claude Code
npx skills add silasvasconcelos/skills -a cursor -a claude-code
```

### List available skills without installing

```bash
npx skills add silasvasconcelos/skills --list
```

### Other useful flags

| Flag | Description |
|---|---|
| `-g, --global` | Install to the user directory instead of the current project. |
| `-a, --agent <name>` | Target specific agents (e.g. `cursor`, `claude-code`, `codex`). Repeatable. |
| `-s, --skill <name>` | Install specific skills by name (use `'*'` for all). Repeatable. |
| `-l, --list` | List available skills without installing. |
| `--copy` | Copy files instead of symlinking into agent directories. |
| `-y, --yes` | Skip all confirmation prompts (CI/CD friendly). |
| `--all` | Install all skills to all agents without prompts. |

Full CLI reference: [skills CLI docs](https://github.com/vercel-labs/skills).

## Usage

Once installed, the skill is available to your agent automatically. Trigger it by describing the task in natural language — for example:

> Generate business documentation for this repository.

To use flags exposed by a skill, mention them in your prompt:

```text
Generate business documentation in docs/, with code evidence, using 3 subagents.
# business-doc → --output=docs --add-code --use-subagents=3
```

See each skill's folder for its full set of flags and behavior.

## Repository layout

```
.
├── README.md
└── <skill-name>/
    ├── SKILL.md          # skill entry point (name + description front matter)
    └── templates/        # optional support files used by the skill
```

To add a new skill, create a new top-level folder with its own `SKILL.md` and add a row to the [Skills](#skills) table above.

## Contributing

Contributions are welcome. New skills should:

- Live in a dedicated top-level folder named in `kebab-case`.
- Include a `SKILL.md` with `name` and `description` front matter.
- Be documented with a row in the [Skills](#skills) table.

## License

MIT
