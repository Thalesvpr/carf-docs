---
type: readme
status: review
updated: 2026-01-22
---

# Templates

Documentos normativos que definem a forma padrao de cada tipo de arquivo no vault. Cada template especifica regras de escrita, limites de tamanho, secoes obrigatorias e padroes proibidos. O plugin de validacao descobre templates dinamicamente pelo frontmatter `type: template` e `template_for: <tipo>`.

Cada tipo possui um TEMPLATE (regras e estrutura) e um EXAMPLE (documento preenchido seguindo o template). A nomenclatura segue o padrao `00X-TYPE-TEMPLATE.md` e `00X-TYPE-EXAMPLE.md` onde X identifica o par.

## Estrutura

| # | Tipo | Template | Example |
|---|------|----------|---------|
| 001 | ADR | [001-ADR-TEMPLATE](./001-ADR-TEMPLATE.md) | [001-ADR-EXAMPLE](./001-ADR-EXAMPLE.md) |
| 002 | README | [002-README-TEMPLATE](./002-README-TEMPLATE.md) | [002-README-EXAMPLE](./002-README-EXAMPLE.md) |
| 003 | RF | [003-RF-TEMPLATE](./003-RF-TEMPLATE.md) | [003-RF-EXAMPLE](./003-RF-EXAMPLE.md) |
| 004 | US | [004-US-TEMPLATE](./004-US-TEMPLATE.md) | [004-US-EXAMPLE](./004-US-EXAMPLE.md) |
| 005 | RNF | [005-RNF-TEMPLATE](./005-RNF-TEMPLATE.md) | [005-RNF-EXAMPLE](./005-RNF-EXAMPLE.md) |
| 006 | UC | [006-UC-TEMPLATE](./006-UC-TEMPLATE.md) | [006-UC-EXAMPLE](./006-UC-EXAMPLE.md) |
| 007 | LEAF | [007-LEAF-TEMPLATE](./007-LEAF-TEMPLATE.md) | [007-LEAF-EXAMPLE](./007-LEAF-EXAMPLE.md) |
