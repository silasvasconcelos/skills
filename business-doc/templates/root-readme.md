<!-- Copy _header.md at top and adjust -->

# Business Documentation — <System Name>

> This documentation describes the system from a **business** perspective.
> For technical details, see the engineering documentation.

## Table of contents

### Global view
- [System overview](./00-visao-geral.md)
- [Glossary](./01-glossario.md)
- [Process map](./02-processos.md)
- [External integrations](./03-integracoes.md)
- [Compliance and LGPD](./04-conformidade.md)
- [KPIs and metrics](./05-kpis.md)
- [Business rules (catalog)](./06-regras-de-negocio.md)
- [Open questions](./99-perguntas-abertas.md)

### Features

| Feature | Summary | Confidence | Owner |
|---|---|---|---|
| [<feature-1>](./features/<slug-1>/README.md) | ... | High/Medium/Low | ... |
| [<feature-2>](./features/<slug-2>/README.md) | ... | ... | ... |

## How to navigate

- Start with **Overview** if you are new to the system.
- Go directly to a **feature** to understand a specific flow.
- Use the **Glossary** whenever you encounter an unknown term.
- Questions about rules: **Business rules** or **Open questions**.

## Conventions

- `[Fact]` — validated in code or test.
- `[Hypothesis]` — inferred, requires confirmation.
- `[Question]` — recorded in `99-perguntas-abertas.md`.
