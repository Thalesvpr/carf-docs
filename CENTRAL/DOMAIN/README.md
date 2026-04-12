---
type: readme
status: approved
updated: 2026-01-24
---

# DOMAIN

Linguagem ubiqua e modelo conceitual do dominio REURB. Define O QUE sao as entidades de negocio, suas relacoes e estados, alinhado com o WORKFLOW-MESTRE.

A documentacao organiza-se em duas areas. Os [conceitos](./CONCEPTS/README.md) definem as 37 entidades do dominio como Unit (unidade habitacional), Holder (titular), Community (comunidade), Tenant (regiao) e Legitimation (processo de regularizacao), estabelecendo vocabulario comum entre equipe tecnica e especialistas de dominio. Os [diagramas](./DIAGRAMS/README.md) fornecem visualizacoes do modelo incluindo aggregates DDD, diagrama ER do banco, fluxo de multi-tenancy e state machines dos workflows.

Regras de negocio que governam validacoes, transicoes de estado e restricoes legais sao documentadas separadamente em [DOMAIN-RULES](../DOMAIN-RULES/README.md). Classes tecnicas como BaseEntity e AggregateRoot pertencem ao codigo-fonte em PROJECTS/GEOAPI/.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (2)

| Pasta | Descrição |
|-------|-----------|
| [CONCEPTS](./CONCEPTS/README.md) | ... |
| [DIAGRAMS](./DIAGRAMS/README.md) | ... |

<!-- CARF-INDEX-END -->
