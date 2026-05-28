<!-- _header.md at the top -->

# Conflicts between business rules

> Conflicts detected during analysis. Each conflict has a stable ID `C-NNN`,
> appears **bidirectionally** in the involved rules, and generates a `Q-NNN` when severity ≥ Medium.

## Summary

| Severity | Count |
|---|---|
| High | 0 |
| Medium | 0 |
| Low | 0 |

## Types considered

- **Direct contradiction** — rules cancel each other for the same trigger.
- **Overlap with distinct criteria** — same event, different decisions.
- **Ambiguous precedence** — unclear which rule takes precedence.
- **Divergent definition** — same concept defined in incompatible ways.
- **Combinatorial incompatibility** — valid in isolation, impossible together.
- **Owner/version divergence** — different owners maintain conflicting versions.

## Conflict list

### C-001 — <short title>
- **Involved rules:** `RN-<feature>-001` ↔ `RN-<other-feature>-005`
- **Type:** direct contradiction
- **Severity:** High
- **Description:** ...
- **Scenario where it appears:** ...
- **Business impact:** ...
- **Affected owners:** area X, area Y
- **Generated open question:** Q-XXX
- **Suggested resolution:**
  - Option A: ...
  - Option B: ...
- **Status:** open | under review | resolved (vXX)

### C-002 — ...

## Reference integrity

Validate before publishing:
- [ ] Each conflict is listed in both involved rules (bidirectional).
- [ ] Each conflict with severity ≥ Medium has a corresponding `Q-NNN`.
- [ ] `06-regras-de-negocio.md` shows the `Conflicts` column populated.
- [ ] No orphan references (link without reverse).
