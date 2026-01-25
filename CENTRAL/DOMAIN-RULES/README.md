---
type: readme
status: approved
updated: 2026-01-24
---

# DOMAIN-RULES

Regras de negocio do dominio REURB. Define COMO as coisas funcionam incluindo base legal, transicoes de estado permitidas e validacoes obrigatorias, alinhado com o WORKFLOW-MESTRE.

Enquanto [DOMAIN](../DOMAIN/README.md) estabelece O QUE sao as coisas atraves de conceitos, DOMAIN-RULES documenta COMO essas coisas se comportam atraves de regras e restricoes. Por exemplo, DOMAIN define o que e uma unidade habitacional; DOMAIN-RULES especifica que uma unidade so pode transicionar para status aprovado se tiver geometria validada e ao menos um titular principal vinculado.

A organizacao segue tres eixos. As [regras legais](./LEGAL/README.md) documentam restricoes da Lei 13.465/2017 e normativas REURB. Os [workflows](./WORKFLOWS/README.md) definem state machines que governam transicoes de status de Unit e Legitimation. As [validacoes](./VALIDATIONS/README.md) catalogam regras de consistencia de dados. Os USE-CASES completos que orquestram multiplos atores estao nos projetos GEOAPI, GEOWEB, GEOGIS e REURBCAD.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (3)

| Pasta | Descrição |
|-------|-----------|
| [LEGAL](./LEGAL/README.md) | ... |
| [VALIDATIONS](./VALIDATIONS/README.md) | ... |
| [WORKFLOWS](./WORKFLOWS/README.md) | ... |

<!-- CARF-INDEX-END -->
