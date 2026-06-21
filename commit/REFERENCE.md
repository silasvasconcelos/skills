# Atomic Commit — Reference

## File categories

Group files before planning commits. Lower priority number = commit earlier.

| Priority | Category | File patterns | Commit type |
| -------- | -------- | ------------- | ----------- |
| 1 | Configuration | `.env.example`, `*.config.*`, config `*.json`, `*.yaml`, `*.toml`, `.gitignore`, `.dockerignore` | `chore` or `build` |
| 2 | Dependencies | Dependency manifests and lockfiles at repo or package roots | `build(deps)` |
| 3 | Database/Migrations | `migrations/`, `**/migrate*`, `schema.*`, `*.sql` | `feat(db)` or `fix(db)` |
| 4 | Types/Interfaces | `types/`, `interfaces/`, `contracts/`, `schemas/` | `feat(types)` |
| 5 | Models/Entities | `models/`, `entities/`, `domain/` | `feat(model)` |
| 6 | Services/Business logic | `services/`, `usecases/`, `handlers/`, `tasks/` | `feat` or `fix` |
| 7 | API/Routes | `routes/`, `controllers/`, `api/`, `endpoints/` | `feat(api)` or `fix(api)` |
| 8 | UI components | `components/`, `views/`, `pages/`, `templates/` | `feat(ui)` or `fix(ui)` |
| 9 | Styles | `*.css`, `*.scss`, `*.less`, `*.styled.*` | `style` |
| 10 | Tests | `*.test.*`, `*.spec.*`, `__tests__/`, `tests/`, `test/` | `test` |
| 11 | Documentation | `*.md`, `docs/`, `README*`, `CHANGELOG*` | `docs` |
| 12 | i18n | `locale/`, `locales/`, translation resource files | `feat(i18n)` or `fix(i18n)` |
| 13 | CI/CD | `.github/`, `.gitlab-ci*`, `Jenkinsfile`, `.circleci/` | `ci` |
| 14 | Other | Everything else | Infer from content |

**Never commit:** `.env`, `credentials.json`, `*.pem`, `*.key`, or other secret files. Warn the user.

### Porcelain status codes

| Code | Meaning |
| ---- | ------- |
| `M` | Modified |
| `A` | Added (staged) |
| `D` | Deleted |
| `??` | Untracked |
| `R` | Renamed |
| `C` | Copied |

## Dependency order

For each file, infer dependencies from imports, config references, and parent-child links (component → styles).

Commit order:

1. Base types/interfaces before implementations
2. Models before services that use them
3. Services before controllers/routes
4. Settings/config before modules that depend on them
5. Utilities before consumers

## Atomicity rules

**Maximum 1–3 files per commit** (prefer single file).

**May group together:**

- Component + its stylesheet
- Test file + file under test
- Interface + implementation (same module)
- Migration + model change (same module)
- Translation files + related source (same module)

**Never mix:**

- Different features
- Bug fixes with features
- Unrelated changes
- Migrations from different modules

**Grouping logic:**

```
For each file in dependency order:
  1. If direct counterpart exists (test, styles), group them
  2. If isolated change, commit alone
  3. If same atomic feature unit, group (max 3)
```

## Conventional Commits

Message language follows `--language`. Types and scopes always English.

### English (`--language=en`)

```
<type>(<scope>): <imperative description, max 72 characters>
```

- Imperative mood: "add", "fix", "implement" — not "adds", "added", "adding"

### Brazilian Portuguese (`--language=pt-BR` or `--language=pt`)

```
<type>(<scope>): <descrição em português, terceira pessoa do presente, máx 72 caracteres>
```

- Third-person present: "adiciona", "corrige", "implementa", "atualiza"

### Commit types

| Type | When to use |
| ---- | ----------- |
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (not CSS) |
| `refactor` | Refactor without feature/fix |
| `perf` | Performance improvement |
| `test` | Add or update tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks |

### Message style: problem focus

Describe **what was solved or added** functionally — not implementation details.

Ask: "What would a non-technical colleague understand from this change?"

#### Fixes

| Avoid (too technical) | Prefer (problem focus) |
| --------------------- | ---------------------- |
| `fix(model): serialize dates in entity export helper` | `fix(model): fix date parsing in base model` |
| `fix(api): add try-catch on login endpoint` | `fix(api): handle authentication errors correctly` |
| `fix(repo): use left join instead of inner join in query` | `fix(repo): fix listing items without association` |
| `fix(handler): validate None before accessing attribute` | `fix(handler): avoid error when processing empty data` |
| `fix(dto): change field type to nullable integer` | `fix(dto): allow optional field in request` |
| `fix(db): add coalesce to avoid null in sum` | `fix(db): fix total calculation with null values` |

#### Features

| Avoid (too technical) | Prefer (functionality focus) |
| --------------------- | ---------------------------- |
| `feat(api): add validation hook on endpoint` | `feat(api): validate permissions on restricted resources` |
| `feat(model): add tenant reference field to entity` | `feat(model): add multi-tenant support to model` |
| `feat(service): implement get_by_id method in repository` | `feat(service): allow lookup by external identifier` |
| `feat(handler): add pagination with offset and limit` | `feat(handler): implement pagination in listing` |
| `feat(dto): create search filter schema with optional fields` | `feat(dto): add search filters` |

#### Refactors

| Avoid (too technical) | Prefer (benefit focus) |
| --------------------- | ---------------------- |
| `refactor(repo): extract private _build_query method` | `refactor(repo): simplify query construction` |
| `refactor(handler): replace loop with inline transform` | `refactor(handler): improve code readability` |
| `refactor(api): move validation to middleware` | `refactor(api): centralize request validation` |

#### Performance

| Avoid (too technical) | Prefer (result focus) |
| --------------------- | --------------------- |
| `perf(repo): add composite index on lookup columns` | `perf(repo): improve identifier lookup performance` |
| `perf(query): switch eager-loading strategy in query` | `perf(query): optimize relationship loading` |
| `perf(api): implement cache with 5 minute TTL` | `perf(api): add cache to reduce queries` |

#### General examples (English)

- `feat(auth): add jwt token validation`
- `fix(api): fix error when fetching nonexistent user`
- `test(user): add unit tests for user service`
- `build(deps): update dependency versions`
- `refactor(db): simplify repository queries`
- `docs(readme): update installation instructions`
- `chore(config): configure environment variables`
- `perf(query): optimize record lookup by tenant`
- `feat(i18n): add portuguese translations for accounts module`
- `feat(admin): register user model in admin panel`

### Message length validation

```
For each message in the plan:
  1. Count full length (type + scope + description)
  2. If <= 72 characters: approved
  3. If > 72 characters: start review process
```

**Review process (max 5 attempts):**

- Use shorter synonyms
- Remove unnecessary words
- Abbreviate scope if possible
- Simplify description while keeping meaning

**Still > 72 after 5 attempts** — show warning and alternatives:

```text
Warning: message exceeds 72 characters (current: XX chars)

Original message:
> feat(authentication): implement jwt token validation with automatic refresh

Alternative suggestions:
[1] feat(auth): add jwt validation with refresh (42 chars)
[2] feat(auth): implement jwt tokens and refresh (40 chars)
[3] feat(auth): validate jwt with auto-refresh (36 chars)

Options:
- Enter a number (1-3) to select a suggestion
- Enter your own message
- Enter 'skip' to keep the original (not recommended)
```

With `--yes`, pick the shortest valid suggestion automatically.

## Plan format

Present plan as numbered table:

```text
┌─────┬──────────────────────────────────────────────────────────────────┐
│  #  │ Commit Plan                                                      │
├─────┼──────────────────────────────────────────────────────────────────┤
│  1  │ chore(config): add environment configuration                     │
│     │ Files: .env.example                                              │
├─────┼──────────────────────────────────────────────────────────────────┤
│  2  │ feat(types): add user entity types                               │
│     │ Files: src/types/user                                            │
├─────┼──────────────────────────────────────────────────────────────────┤
│  3  │ feat(model): implement user model                                │
│     │ Files: src/models/user                                           │
├─────┼──────────────────────────────────────────────────────────────────┤
│  4  │ test(user): add user service tests                               │
│     │ Files: src/services/user.test, src/services/user                 │
└─────┴──────────────────────────────────────────────────────────────────┘
```

**Confirmation prompt** (skip with `--yes` or `--dry-run`):

> This will create **X commits** for **Y files**. Proceed? (yes/no/edit)

## Hook and amend edge cases

| Situation | Action |
| --------- | ------ |
| Pre-commit hook fails | Stop; fix reported issues; create new commit — never amend unless user explicitly requests amend |
| Hook auto-formats files | Stage formatting fixes; include in same commit if hook re-runs cleanly, else new commit |
| Commit rejected mid-plan | Stop remaining commits; report which succeeded |
| User asks to amend | Only if HEAD not pushed (or user accepts force push) and user explicitly requested amend |
| `.env` in changed files | Exclude; warn — commit `.env.example` only if intentional |

## Final summary

After all commits (and optional push):

```text
Atomic Commits Complete

Total commits: X
Total files committed: Y
Pushed: yes/no

Commit history:
abc1234 feat(types): add user entity types
def5678 feat(model): implement user model
ghi9012 feat(service): add user service
...

Run 'git log --oneline -X' to review all commits.
```
