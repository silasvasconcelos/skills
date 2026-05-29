---
name: business-doc
description: Generates business (non-technical) documentation from an existing codebase. Organizes by feature/user story, includes Mermaid flows, glossary, business rules, KPIs, integrations, compliance, and open questions. Supports parallel analysis with subagents. With the `--features` flag, generates one self-contained document per identified feature following the `feature.md` template (filename = feature name). With the `--frs` flag, generates Software Requirements documentation (RF/RNF) instead — one document per feature — and can convert existing business documentation to FRS via `--frs --from-existing={path}`. The `--language` flag (default `en`) controls the output language.
---

# Skill: business-doc

Specialist in **business documentation** from source code.
Written for **business, product, and operations** readers — not developers.

> Business documentation is useful for people who make business decisions.
> If someone from sales, finance, or operations cannot understand it, simplify it.

---

## CLI / Accepted flags

Invocation:

```
business-doc [--output=docs] [--add-code] [--use-subagents=3] [--features] [--frs] [--from-existing={path}] [--language=en]
```

| Flag | Default | Description |
|---|---|---|
| `--output={path}` | `docs` | Root directory where documentation will be generated. Created if it does not exist. |
| `--add-code` | `false` (off) | When absent, **forbidden** to cite file paths, classes, functions, endpoints, SQL, snippets. Business language only. When present, allowed to add a `## Technical evidence` block at the end of each document with references. |
| `--use-subagents={N}` | `3` | Maximum number of parallel subagents to map/analyze features. `0` disables parallelism. |
| `--features` | `false` (off) | **Per-feature mode**. Documentation **must** be generated **by feature**: **one self-contained document per identified feature**, following the `feature.md` template. The **file name is the feature name** and each file contains the full documentation of that feature (see "Features mode" section). |
| `--frs` | `false` (off) | **Software Requirements mode**. Generates **only** documents in the FRS pattern (RF / RNF / acceptance criteria / traceability), **one document per feature**. Output structure differs from business mode (see "FRS mode" section). |
| `--from-existing={path}` | — | Used **together with `--frs`**. Instead of analyzing code, reads **already generated** business documentation at `{path}` (e.g. `docs/`, `documentacao/`) and produces the FRS equivalent. Code is used only for cross-validation and evidence extraction when `--add-code` is also present. |
| `--language={code}` | `en` | Output language of the documentation (e.g. `en`, `pt`, `pt-BR`, `es`). All generated content — titles, body text, tables, diagram labels — is written in this language. File/folder slugs stay in `kebab-case`. |

If the user does not pass flags, assume the defaults above and **declare** at the start of execution:

> "Generating business documentation in `docs/`, without code evidence, using 3 subagents, language `en`."

In Features mode, declare:

> "Generating **per-feature** business documentation in `docs/`, one document per feature following the `feature.md` template, using N subagents, language `<code>`."

In FRS mode, declare:

> "Generating **Software Requirements (FRS)** documentation in `docs/`, one document per feature, using N subagents, language `<code>`." (and, if `--from-existing`, "converting from `<path>`").

---

## Default mode: BUSINESS (no code)

When `--add-code` is **not** present:

- **Forbidden** to mention: file name, path, function, class, module, endpoint, table, column, SQL, payload JSON, framework, library, programming language.
- **Allowed**: system name, feature name, process name, role/persona, business rule, metric, integration described by **purpose** (e.g. "email delivery system" instead of "SendGrid via `EmailService`").
- Language: simple, direct, no technical jargon.
- Every unvalidated statement must fall into one of three categories: **Fact**, **Hypothesis**, **Question** (best practice #16).

When `--add-code` **is** present:

- Add a `## Technical evidence` section at the end of each document listing files, modules, endpoints, and tests that support the content.
- The main body stays in business language; code goes **only** in the appendix.

---

## Features mode (`--features`)

When `--features` is present, documentation **must** be generated **by feature**: the skill produces **one self-contained document per identified feature**, instead of splitting each feature into multiple files (`README.md`, `user-stories.md`, etc.).

### Features principles
- **One feature = one file**, following the `feature.md` template (required).
- The **file name is the feature name** in `kebab-case` (e.g. `user-management.md`, `recurring-subscription.md`, `order-approval.md`).
- Each file contains the **identified feature** in full: overview, business objectives, actors, AS-IS, TO-BE, business rules, use cases, conceptual data model, configurable domains, non-functional requirements, out of scope, glossary, references.
- Files are written entirely from the `feature.md` template — **do not** improvise the structure.
- Business mode rules still apply: no code in the body unless `--add-code` is present (then add a `## Technical evidence` block at the end of each feature file).
- Output language follows `--language` (default `en`).

### Output structure in Features mode

```
{output}/
├── README.md                            # navigable index linking each feature file
├── 00-visao-geral.md                    # business objective, context, personas
├── 01-glossario.md                      # global terms and acronyms
├── 99-perguntas-abertas.md              # questions, hypotheses, gaps
└── features/
    ├── <feature-name-1>.md              # full feature doc (feature.md template)
    ├── <feature-name-2>.md
    └── ...
```

> The per-feature **subfolders** (`features/<slug>/README.md`, `user-stories.md`, `use-cases.md`, `business-rules.md`, `flows.md`, `examples.md`) are **not** generated in Features mode. All of that content is consolidated into the single `features/<feature-name>.md` file. Global macro files `02-processos.md`..`07-conflitos-de-regras.md` are optional in this mode; generate them only if they add executive value, otherwise reference everything from the feature files and `README.md`.

### Templates used in Features mode
- `feature.md` — one document per feature (required, filename = feature name).
- `overview.md`, `glossary.md`, `open-questions.md`, `root-readme.md` — reused for the global files.

> `--features` and `--frs` are mutually exclusive. If both are passed, **declare** the conflict and ask the user which one to use before proceeding.

---

## FRS mode (`--frs`)

When `--frs` is present, the skill generates **exclusively** documentation in the **Functional Requirements Specification** pattern. Macro business structure (processes, KPIs, conflicts, etc.) is **not** generated — except the minimum needed for traceability (overview, glossary, global RNFs, open questions).

### FRS principles
- **One feature = one document** at `features/<slug>/frs.md`.
- Each document contains: identification, actors, pre/post-conditions, **RFs** (atomic, testable), **feature-specific RNFs**, main flow, exceptions, data, integrations, traceability, checklist, and history.
- Stable, unique IDs:
  - Feature: `FUNC-<NNN>`
  - Functional requirement: `RF-<slug>-<NNN>`
  - Non-functional requirement (feature): `RNF-<slug>-<NNN>`
  - Non-functional requirement (global): `RNF-<NNN>`
- **Imperative** language ("The system shall…") and **unambiguous** ("shall" instead of "may/might").
- Each RF has **Gherkin acceptance criteria** (Given/When/Then).
- Each RNF has a **numeric metric** + **verification method**.
- Mandatory priority:
  - RF → MoSCoW (Must / Should / Could / Won't).
  - RNF → Critical / High / Medium / Low.
- Every rule remains marked as `[Fact]` / `[Hypothesis]` / `[Question]` when applicable.
- Business mode rules (`--add-code` or not) still apply: no code in the body unless `--add-code` is present.

### Output structure in FRS mode

```
{output}/
├── README.md                            # navigable FRS index
├── 00-visao-geral.md                    # objective, scope, personas, summary glossary
├── 01-glossario.md                      # terms and acronyms
├── 08-requisitos-nao-funcionais.md      # GLOBAL RNFs (valid for the whole product)
├── 99-perguntas-abertas.md              # questions, hypotheses, gaps
└── features/
    ├── <feature-slug-1>/
    │   └── frs.md                       # complete FRS for the feature
    ├── <feature-slug-2>/
    │   └── frs.md
    └── ...
```

> Files `02-processos.md`, `03-integracoes.md`, `04-conformidade.md`, `05-kpis.md`, `06-regras-de-negocio.md`, `07-conflitos-de-regras.md` and the subfolders `user-stories.md` / `use-cases.md` / `business-rules.md` / `flows.md` / `examples.md` are **not** generated in FRS mode. Equivalent content goes inside the feature's `frs.md` or is referenced in traceability.

### Templates used in FRS mode
- `frs.md` — one document per feature (required).
- `non-functional-requirements.md` — global RNFs.
- `overview.md`, `glossary.md`, `open-questions.md`, `root-readme.md` — reused.

### Conversion from existing doc (`--frs --from-existing={path}`)

When both flags are present:

1. **Do not** scour code as the primary source. Read content from `{path}` (expected structure: default output of this skill in business mode).
2. Map, per feature found at `{path}/features/<slug>/`:
   - `README.md` → FRS sections 2 (overview) and 4 (actors).
   - `user-stories.md` → each US becomes or anchors a corresponding RF; keep ID `US-<slug>-NNN` in **Traceability**.
   - `use-cases.md` → use cases compose the step-by-step and main flow of each RF; keep ID `UC-<slug>-NNN`.
   - `business-rules.md` → enter as "Applicable business rules" on RFs and/or become pre/post-conditions; keep ID `RN-<slug>-NNN`.
   - `flows.md` → Mermaid diagrams go to FRS section 9 (main flow).
   - `examples.md` → scenarios compose Gherkin acceptance criteria for each RF.
3. Map global content:
   - `00-visao-geral.md` → FRS `00-visao-geral.md` (condensed).
   - `01-glossario.md` → FRS `01-glossario.md` (copy + curation).
   - `04-conformidade.md` + `05-kpis.md` + any cross-cutting requirement → feed `08-requisitos-nao-funcionais.md` (security, LGPD, performance, observability).
   - `06-regras-de-negocio.md` / `07-conflitos-de-regras.md` → do not copy wholesale; each rule becomes a reference (`RN-*`) on the RFs where it applies. Unresolved conflicts become entries in `99-perguntas-abertas.md`.
   - `99-perguntas-abertas.md` → merge with new questions raised by the conversion.
4. **Cross-validation:** flag when a US/UC/RN in the existing doc cannot be mapped to any RF (record as `Q-NNN`). Also flag RFs generated without traceable origin (forbidden in `--from-existing` mode: every RF must point to US/UC/RN from the source).
5. **Do not invent** RFs/RNFs not supported by the existing doc — only reorganize and formalize. Gaps become open questions.
6. If `--add-code` is also present, validate each RF against code evidence and fill `## Technical evidence` at the end of the feature FRS.

### When the user asks for conversion only
If the user asks to "convert the current documentation to FRS" without citing a path, assume:
- Source: `documentacao/` (preferred) or `docs/` (fallback) — use whichever exists first in the repo.
- Destination: `docs-frs/` to avoid overwrite.
- Declare the choice before starting and ask for confirmation if both sources exist.

---

## Output structure (default business mode — without `--frs`)

Generate the tree below inside `{output}/` (default `docs/`). For `--frs` mode, see the "FRS mode" section above.

```
{output}/
├── README.md                          # navigable index
├── 00-visao-geral.md                  # business objective, context, personas
├── 01-glossario.md                    # terms, acronyms, domain
├── 02-processos.md                    # macro process map (Mermaid)
├── 03-integracoes.md                  # external systems and failure impact
├── 04-conformidade.md                 # LGPD, audit, retention, policies
├── 05-kpis.md                         # indicators, formulas, owners
├── 06-regras-de-negocio.md            # numbered list, owner, version, conflicts
├── 07-conflitos-de-regras.md          # conflicting rules, severity, resolution
├── 99-perguntas-abertas.md            # questions, hypotheses, gaps
└── features/
    ├── <feature-slug-1>/
    │   ├── README.md                  # feature summary
    │   ├── user-stories.md            # user stories
    │   ├── use-cases.md               # detailed use cases
    │   ├── business-rules.md          # feature-specific rules
    │   ├── flows.md                   # Mermaid flows
    │   └── examples.md                # real scenarios and exceptions
    ├── <feature-slug-2>/
    │   └── ...
    └── ...
```

### Organization rules per feature

- Each **feature** or **macro user story** becomes **one folder** under `features/`.
- Slug in `kebab-case`, derived from the business name (e.g. `user-management`, `recurring-subscription`, `order-approval`).
- Group by **business capability**, not technical module. Inspired by market practice (BIAN, DDD Bounded Context, SAFe Capabilities, Event Storming).
- If a feature has distinct subdomains, create subfolders: `features/payments/pix/`, `features/payments/card/`.
- File names always in **kebab-case**. Document **content** is written in the `--language` language (default `en`); slugs/file names stay in `kebab-case` regardless of language.

---

## Mermaid: required for flows

Each `features/<slug>/flows.md` **must** contain at least one Mermaid diagram representing the business flow. Use the most appropriate type:

- `flowchart` — decision flow / operational process
- `sequenceDiagram` — interaction between personas / external systems
- `stateDiagram-v2` — business entity lifecycle (e.g. Order: created → paid → delivered → completed)
- `journey` — end-to-end user journey
- `erDiagram` — only when `--add-code` (technical structure)

Diagram rules:

- Labels in business language, **never** function or endpoint names.
- Always mark decisions, exceptions, and approvals.
- Limit: ~15 nodes per diagram. If exceeded, split into subflows.

`02-processos.md` (root) must contain a **macro map** linking features — a "forest" view for executives.

---

## Generation process

> The phases below describe **default business mode**. In `--frs` mode, see the variation at the end of this section.

### Phase 1 — Reconnaissance (always serial)
1. Detect stack, modules, context, and entry point.
2. Identify candidate **business capabilities** (list of slugs).
3. Detect external integrations, jobs, queues, events, schemas, roles/permissions.
4. Detect compliance evidence (LGPD, audit, sensitive logs).
5. Produce the **folder plan** under `features/`.

### Phase 2 — Analysis per feature (parallel via subagents)
If `--use-subagents=N` and `N > 0`:

- Distribute features across `min(N, total_features)` subagents.
- Each subagent receives **one or more features** and generates all files for the corresponding folder.
- Each subagent receives the **mode** (`--add-code` or not) and must respect it.
- Each subagent returns: list of extracted business rules, candidate KPIs, integrations touched, questions raised.

If `--use-subagents=0`: generate serially, one feature at a time.

**Base prompt** for the subagent (use when dispatching via `Task` with `subagent_type=explore` or `generalPurpose`):

> Generate **business** documentation for feature `<slug>` in the repository.
> - Mode: `<business-only | with-technical-evidence>`.
> - Output: `{output}/features/<slug>/` with `README.md`, `user-stories.md`, `use-cases.md`, `business-rules.md`, `flows.md`, `examples.md`.
> - Use templates in `.cursor/skills/business-doc/templates/`.
> - Language: `<--language>` (default English), simple, no technical jargon.
> - Include at least one Mermaid diagram in `flows.md`.
> - Mark each statement as Fact / Hypothesis / Question.
> - **Do not** invent features without evidence.
> - Return: extracted rules, candidate KPIs, integrations, questions.

### Phase 3 — Consolidation (serial)
- Aggregate rules, KPIs, integrations, and questions from subagents.
- Write root files: `00..06` and `99`.
- Generate index `README.md` with links to each feature folder.
- Generate the macro diagram in `02-processos.md`.

### Variation for `--features` mode

**Phase 1 — Reconnaissance** — same as business mode (detect stack, identify business capabilities, produce the feature list).

**Phase 2 — Per-feature generation (parallel)**
- Each subagent generates **a single file**: `features/<feature-name>.md` (filename = feature name in `kebab-case`) from the `feature.md` template.
- Features mode subagent base prompt:

  > Generate the **per-feature** business document for feature `<feature-name>`.
  > - Mode: `<business-only | with-technical-evidence>`.
  > - Single output: `{output}/features/<feature-name>.md` using template `.cursor/skills/business-doc/templates/feature.md`.
  > - The file name **is** the feature name (`kebab-case`).
  > - Fill **all** template sections with the identified feature: overview, objectives, actors, AS-IS, TO-BE, business rules, use cases, data model, configurable domains, RNFs, out of scope, glossary, references.
  > - Include at least one diagram (Mermaid or ASCII) in the AS-IS/TO-BE sections.
  > - Mark each statement as Fact / Hypothesis / Question. **Do not** invent content without evidence.
  > - Language: `<--language>` (default English), simple, no technical jargon.
  > - Return: extracted rules, candidate KPIs, integrations, questions.

**Phase 3 — Consolidation**
- Generate `00-visao-geral.md`, `01-glossario.md`, `99-perguntas-abertas.md`, and index `README.md` linking each `features/<feature-name>.md`.
- Aggregate rules, questions, and conflicts across features; record conflicts in `99-perguntas-abertas.md` (no separate `07-conflitos-de-regras.md` unless it adds executive value).

### Variation for `--frs` mode

**Phase 1 — Reconnaissance**
- If `--from-existing={path}`: list `features/*/` under `{path}` and treat each slug as an already identified feature. Skip code-based detection (except for `--add-code`).
- Otherwise: same as business mode, but reconnaissance output is only the feature list + actors + high-level data/integrations.

**Phase 2 — FRS generation per feature (parallel)**
- Each subagent generates **a single file**: `features/<slug>/frs.md` from the `frs.md` template.
- FRS subagent base prompt:

  > Generate the **FRS** (Functional Requirements Specification) for feature `<slug>`.
  > - Mode: `<business-only | with-technical-evidence>`.
  > - Source: `<code | {from-existing}/features/<slug>/>`.
  > - Single output: `{output}/features/<slug>/frs.md` using template `.cursor/skills/business-doc/templates/frs.md`.
  > - Each RF must be atomic, testable, with Gherkin acceptance criteria.
  > - Each RNF must have a numeric metric and verification method.
  > - Mandatory priority: MoSCoW (RF) and Critical/High/Medium/Low (RNF).
  > - IDs: `FUNC-NNN`, `RF-<slug>-NNN`, `RNF-<slug>-NNN`. Fill traceability with `US-*`, `UC-*`, `RN-*` when coming from existing doc.
  > - If `--from-existing`, **do not invent** RF/RNF without traceable origin; gaps become `Q-NNN`.
  > - Language: `<--language>` (default English), imperative, unambiguous.
  > - Return: list of generated RFs and RNFs, questions, RFs without origin (if applicable).

**Phase 3 — Consolidation**
- Generate `00-visao-geral.md`, `01-glossario.md`, `08-requisitos-nao-funcionais.md`, `99-perguntas-abertas.md`, and index `README.md`.
- Validate integrity: every `RF-*` must have at least one acceptance criterion; every `RNF-*` must have a metric. Abort/warn otherwise.
- Final table in chat: totals for FUNC, RF, RNF, questions, RFs without origin (if `--from-existing`).

---

## Applied best practices (mandatory checklist)

Before finishing, validate that the documentation meets all 20 practices:

| # | Practice | Where it appears |
|---|---|---|
| 1 | Business objective | `00-visao-geral.md` |
| 2 | Users and profiles | `00-visao-geral.md` + each `features/*/README.md` |
| 3 | Business processes | `02-processos.md` + `features/*/flows.md` |
| 4 | User stories | `features/*/user-stories.md` |
| 5 | Use cases | `features/*/use-cases.md` |
| 6 | Explicit business rules + **conflicts** | `06-regras-de-negocio.md` + `07-conflitos-de-regras.md` + `features/*/business-rules.md` |
| 7 | Glossary | `01-glossario.md` |
| 8 | KPIs and metrics | `05-kpis.md` |
| 9 | External integrations | `03-integracoes.md` |
| 10 | Compliance (LGPD etc.) | `04-conformidade.md` |
| 11 | Standardization | kebab-case names, fixed structure, version in header |
| 12 | Access control / history | header with `Owner` and `Version` on each doc |
| 13 | Periodic review | header with `Last review` and `Next review` |
| 14 | No irrelevant detail | review and remove |
| 15 | Simple language | mandatory in business mode |
| 16 | Fact/Hypothesis/Question separated | tags `[Fact]` `[Hypothesis]` `[Question]` |
| 17 | Real examples | `features/*/examples.md` |
| 18 | Owners | header on each doc |
| 19 | Centralization | everything under `{output}/` |
| 20 | Part of the process | generated via skill, versioned in repo |

---

## Mandatory header on every document

Every generated `.md` file starts with:

```
---
title: <Document title>
feature: <feature-slug or "global">
owner: <TBD — see 99-perguntas-abertas.md>
status: draft
version: 0.1.0
last_revision: <YYYY-MM-DD>
next_revision: <YYYY-MM-DD + 90 days>
sources:
  - codebase ({short-commit-hash if available})
---
```

Right after the header, one **Confidence** line: `High | Medium | Low` — based on how much evidence existed in the code.

---

## Templates

Templates live in `.cursor/skills/business-doc/templates/`:

- `feature.md` — used **only** in `--features` mode (one self-contained document per feature; filename = feature name).
- `feature-readme.md`
- `user-story.md`
- `use-case.md`
- `business-rule.md`
- `flow.md`
- `example.md`
- `overview.md`
- `glossary.md`
- `processes.md`
- `integrations.md`
- `compliance.md`
- `kpis.md`
- `business-rules-index.md`
- `conflicts.md`
- `open-questions.md`
- `root-readme.md`
- `frs.md` — used **only** in `--frs` mode (one per feature).
- `non-functional-requirements.md` — used **only** in `--frs` mode (global RNFs).

**Always** copy from the template and fill in. Do not improvise structure.

---

## Quality rules

- Every feature has a **confidence level** (High / Medium / Low).
- Every business rule has a stable **ID**: `RN-<feature>-<NNN>`.
- Every user story has ID: `US-<feature>-<NNN>`.
- Every use case has ID: `UC-<feature>-<NNN>`.
- Every question has ID: `Q-<NNN>` and a backlink from the originating feature.
- No generic text like "this system is a modern, scalable API".
- If no test covers the rule, mark as `[Hypothesis]` or `[Question]` — never `[Fact]`.

---

## Business rule conflict detection (mandatory)

During consolidation, the skill **must** compare all extracted rules (`RN-*`) and identify **conflicts**. A conflict exists when two or more rules:

- **Contradict** each other directly (e.g. `RN-orders-003` requires approval above R$ 1,000, `RN-checkout-007` allows automatic purchase above R$ 500).
- **Overlap** with different criteria for the same event (same trigger, different decisions).
- Have **ambiguous precedence** (unclear which rule wins).
- **Define the same concept differently** (e.g. "active customer" defined in two incompatible ways).
- Become **incompatible in combination** (each valid alone, together they produce an impossible state).
- Have **conflicting versions/owners** for the same situation.

### Conflict classification
| Type | Suggested severity |
|---|---|
| Direct contradiction | High |
| Overlap with different criteria | High |
| Ambiguous precedence | Medium |
| Divergent definition | Medium |
| Combinatorial incompatibility | High |
| Owner/version disagreement | Low |

### Where to record

1. **New global document**: `{output}/07-conflitos-de-regras.md` (use template `conflicts.md`).
2. **Global catalog** `06-regras-de-negocio.md`: add `Conflicts` column listing IDs.
3. **Per feature** `features/<slug>/business-rules.md`: add `**Detected conflicts**` block on each involved rule.
4. **Open questions** `99-perguntas-abertas.md`: each Medium/High severity conflict becomes `Q-NNN` with a suggested recipient.

### Bidirectional reference (mandatory)

Every link between artifacts must be **bidirectional**. When creating A → B, create the reverse B → A in the same step.

Mandatory bidirectional pairs:

| From | To | Where |
|---|---|---|
| `RN-x` ↔ `RN-y` (conflict) | mutual | `Detected conflicts` section on both |
| `RN-x` ↔ `US-y` | mutual | "Applicable rules" on US and "Related stories" on rule |
| `RN-x` ↔ `UC-y` | mutual | "Applicable rules" on UC and "Related cases" on rule |
| `US-x` ↔ `UC-y` | mutual | "Related cases" and "Related stories" sections |
| `Q-x` ↔ originating artifact | mutual | "Origin" on question, "Open questions" on artifact |
| `KPI-x` ↔ feature | mutual | "Related KPIs" on feature, "Features" on KPI |
| Integration ↔ feature | mutual | listed in `03-integracoes.md` and in `features/<slug>/README.md` |

Include on each `RN-*`:
- `**Related to:**` list of IDs (`US-*`, `UC-*`, `RN-*`, `Q-*`)
- `**Detected conflicts:**` list of IDs with link and conflict type

The skill **does not** finish while broken references (link without reverse) exist. Validation: generate an integrity table during consolidation and abort/warn if orphan links exist.

### In the final chat summary
Include block:
- **Conflicts detected:** N (High: X, Medium: Y, Low: Z)
- Top 3 critical conflicts by severity
- Total bidirectional references validated: N (orphans: 0 required)

---

## Anti-patterns (forbidden)

- Citing files/functions/endpoints **outside** `## Technical evidence` when `--add-code` is omitted.
- Mixing features by technical layer (e.g. folder `features/controllers`, `features/services`). Folders are by **business capability**.
- Mermaid diagrams with class/function names in business mode.
- Document without header, owner, or date.
- Inventing persona, KPI, rule, or integration without evidence.
- Copying large code blocks in the document body.
- Writing in a language other than the one set by `--language` (default `en`).

---

## Chat output (execution summary)

When finished, print in chat:

**Default business mode:**
1. Generated folder (path).
2. List of detected features and slugs.
3. Totals: rules, stories, use cases, questions.
4. Top 5 critical questions to validate with stakeholders.
5. Suggested next steps (validation, owner assignment, review).

**`--features` mode:**
1. Generated folder (path) and language.
2. List of generated feature files (`features/<feature-name>.md`).
3. Totals: features, rules, use cases, questions.
4. Top 5 critical questions to validate with stakeholders.
5. Suggested next steps.

**`--frs` mode:**
1. Generated folder (path) and source (code or `--from-existing={path}`).
2. List of features (FUNC-NNN + slug + title).
3. Totals: `RF`, `RNF` (feature) + `RNF` (global), questions (`Q-NNN`).
4. Features without complete Gherkin acceptance criteria (need review).
5. With `--from-existing`: list of US/UC/RN from source **not** mapped to any RF.
6. Top 5 critical questions.

Never print file contents — summary only.
