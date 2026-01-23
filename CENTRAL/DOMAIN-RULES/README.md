---
type: readme
status: review
updated: 2026-01-22
---

# DOMAIN-RULES

Regras de negocio do dominio REURB. Define COMO as coisas funcionam incluindo base legal, transicoes de estado permitidas e validacoes obrigatorias.

Enquanto [DOMAIN](../DOMAIN/README.md) estabelece O QUE sao as coisas atraves de conceitos e glossario, DOMAIN-RULES documenta COMO essas coisas se comportam atraves de regras, restricoes e invariantes. Por exemplo, DOMAIN define o que e uma unidade habitacional; DOMAIN-RULES especifica que uma unidade so pode transicionar para status aprovado se tiver geometria validada e ao menos um titular principal vinculado.

A organizacao segue tres eixos complementares. As [regras legais](./LEGAL/README.md) documentam restricoes derivadas da legislacao REURB incluindo Lei 13.465/2017, decretos regulamentadores e normativas municipais, mapeando artigos especificos para regras de sistema. Os [workflows](./WORKFLOWS/README.md) definem maquinas de estado puras que governam transicoes validas entre status de entidades como unidade, processo de legitimacao e sincronizacao, especificando pre-condicoes, pos-condicoes e eventos disparados. As [validacoes](./VALIDATIONS/README.md) catalogam regras de consistencia de dados incluindo formatos obrigatorios, intervalos permitidos e validacoes cruzadas entre entidades.

Os workflows aqui documentados diferem dos processos end-to-end em [REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS](../REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/README.md). DOMAIN-RULES/WORKFLOWS foca na maquina de estados pura de uma entidade isolada, enquanto PROCESS-WORKFLOWS documenta fluxos completos de negocio que envolvem multiplos atores, sistemas e etapas coordenadas.

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
