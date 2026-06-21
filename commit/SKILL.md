---
name: commit
description: >-
  Plans and executes atomic Conventional Commits in dependency order (1–3 files each).
  Use when the user runs /commit, asks to split changes into atomic commits,
  or wants Conventional Commits with --yes, --push, --dry-run, or --language.
---

# Atomic Commit

Only run when the user explicitly requests commits (`/commit`, "commit this", "split into atomic commits"). Do not commit unprompted.

If user or project git rules conflict with this skill, follow the stricter rule.

## Quick start

```text
/commit                          # plan + confirm
/commit --yes                    # execute without confirm
/commit --dry-run                # plan only
/commit --language=pt-BR --yes   # Portuguese messages, auto-run
/commit --yes --push             # commit + push upstream
```

## User input

```text
$ARGUMENTS
```

Consider `$ARGUMENTS` before proceeding. User may specify scope filters, custom messages, or files to include/exclude.

## Flags

| Flag | Default | Behavior |
| ---- | ------- | -------- |
| `--language={code}` | `en` | Message language. `en` = English imperative. `pt-BR` / `pt` = Brazilian Portuguese third-person present. Types and scopes stay English. |
| `--yes` | off | Skip confirmation; execute plan immediately. |
| `--push` | off | Push after all commits succeed. No upstream → `git push -u origin HEAD`. |
| `--dry-run` | off | Show plan only. No stage, commit, or push. |

## Workflow

1. **Inspect** — Run in parallel:
   - `git status`
   - `git diff` (and `git diff --staged` if staged changes exist)
   - `git log -5 --oneline`
   Abort if merge conflicts. Clean tree → tell user nothing to commit. Verify correct branch.
2. **Categorize** — Group changed files by type and purpose. See [REFERENCE.md](REFERENCE.md#file-categories).
3. **Dependencies** — Order commits: types → models → services → routes → UI. See [REFERENCE.md](REFERENCE.md#dependency-order).
4. **Plan** — Atomic commits: max 1–3 files; never mix unrelated features or fix+feat. See [REFERENCE.md](REFERENCE.md#atomicity-rules).
5. **Messages** — Conventional Commits, max 72 chars, problem-focused. See [REFERENCE.md](REFERENCE.md#conventional-commits).
6. **Validate length** — If > 72 chars, shorten (max 5 attempts). Still too long → offer 3 alternatives; with `--yes`, pick shortest.
7. **Present plan** — Numbered table: `#`, message, files. See [REFERENCE.md](REFERENCE.md#plan-format).
8. **Confirm** — Ask unless `--yes` or `--dry-run`. Options: yes / no / edit.
9. **Execute** — For each commit (skip if `--dry-run`):
   ```sh
   git add <files>
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>
   EOF
   )"
   ```
   After each: `git log -1 --oneline`. Show `[X/Y] Committed: <message>`.
   - Commit fails or hook rejects → stop; fix issue; create **new** commit (never amend unless user explicitly requests amend and all amend conditions are met).
   - Hook auto-modifies files → include fixes in a follow-up commit; do not amend unless allowed.
10. **Push & summary** — Push only if `--push` or user explicitly asked. Report totals and `git log --oneline` output.

## Safety rules

- Never commit `.env`, credentials, secrets, or key files; warn user and exclude from plan.
- Never update git config.
- Respect `.gitignore`; include deleted files with appropriate messages.
- Never force push unless user explicitly requests.
- Never skip hooks (`--no-verify`) unless user explicitly requests.
- Never amend unless user explicitly requests it and HEAD was not pushed (or user accepts force push).
- Push only when `--push` or user explicitly asked; push failure → stop; do not retry force push.

## Edge cases

| Situation | Action |
| --------- | ------ |
| No changes | "Working directory is clean. Nothing to commit." |
| Untracked only | Ask to track first; with `--yes`, include in plan |
| > 20 files | Warn; suggest splitting into sessions |
| Binary files | Separate commit (e.g. `chore: add logo assets`) |
| Secret files in diff | Exclude; warn user |

Full edge-case list and message examples: [REFERENCE.md](REFERENCE.md).
