---
title: Non-functional requirements (global)
feature: global
owner: TBD
status: draft
version: 0.1.0
last_revision: <YYYY-MM-DD>
next_revision: <YYYY-MM-DD>
sources:
  - codebase (<short-commit>)
---

**Confidence:** High | Medium | Low

# Non-functional requirements — Global

> NFRs that apply to the **entire product**. Feature-specific NFRs live in `features/<slug>/frs.md` (section 8).

## Categories used
Performance · Security · Availability · Scalability · Usability · Reliability · Compatibility · Maintainability · Legal/Compliance

## Index
| ID | Category | Title | Priority | Verification | Affected features |
|---|---|---|---|---|---|
| RNF-001 | Performance | <title> | Critical | Load test | FUNC-001, FUNC-002 |
| RNF-002 | Security | <title> | Critical | Pentest | All |

---

## RNF-001: <Category> — <Title>
- **Description:** The system must <property> under <condition> with <metric>.
- **Category:** <category>
- **Metric:**
  - Target value: <number + unit>
  - Minimum acceptable value: <number + unit>
  - Unit: <ms | req/s | % | concurrent users | ...>
- **Application conditions:** <environment / scenario>
- **Verification method:** <how it will be tested>
- **Priority:** Critical | High | Medium | Low
- **Affected features:** FUNC-NNN, FUNC-NNN (or "All")
- **Dependencies:** RNF-NNN
- **Source:** <stakeholder / standard / contract>
- **Confidence:** High | Medium | Low

## RNF-002: ...
