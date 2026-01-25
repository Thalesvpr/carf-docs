---
type: readme
status: review
updated: 2026-01-24
---

# USE-CASES - REURBCAD

Casos de uso do aplicativo mobile REURBCAD, focados na PARTE 3 do workflow: operacao em campo.

## Referencia

Todos os UCs implementam o [WORKFLOW-MESTRE](../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## PARTE 3: Operacao em Campo

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P3-001](./UC-P3-001-autenticar-agente-campo/README.md) | Autenticar Agente | Login via Keycloak |
| [UC-P3-002](./UC-P3-002-download-pacote-temporario/README.md) | Download Pacote | Pacote unico e temporario |
| [UC-P3-003](./UC-P3-003-selecionar-comunidade/README.md) | Selecionar Comunidade | Carregar mapa e poligonos |
| [UC-P3-004](./UC-P3-004-operar-em-campo/README.md) | Operar em Campo | GPS, formularios, assinatura, QR |
| [UC-005](./UC-005-sincronizar-dados-offline/README.md) | Sincronizar Dados | Push/pull com backend |

## Fluxo Sequencial

```
[PARTE 2] -> UC-P3-001 -> UC-P3-002 -> UC-P3-003 -> UC-P3-004 -> UC-005
```

## Casos de Uso Complementares

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-003](./UC-003-vincular-titular-unidade/README.md) | Vincular Titular | Associar titular a unidade (pre-publicacao) |
| [UC-009](./UC-009-gerenciar-processo-legitimacao/README.md) | Legitimacao | Processo pos-workflow (fase separada) |

## Relacionamentos

- **GEOAPI**: Backend que fornece pacotes e recebe sincronizacao
- **GEOGIS**: Origem dos dados publicados (PARTE 2)
- **GEOWEB**: Portal para visualizacao e aprovacao
