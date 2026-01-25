---
type: readme
status: review
updated: 2026-01-24
---

# USE-CASES - GEOAPI

Casos de uso do backend GEOAPI, focados na PARTE 1 do workflow: recebimento e processamento de ortofotos.

## Referencia

Todos os UCs implementam o [WORKFLOW-MESTRE](../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## PARTE 1: Entrega e Processamento de Ortofotos

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P1-001](./UC-P1-001-entregar-ortofoto/README.md) | Entregar Ortofoto | Analista de Drone envia ortofoto |
| [UC-P1-002](./UC-P1-002-processar-ortofoto/README.md) | Processar Ortofoto | Backend processa e otimiza |
| [UC-P1-003](./UC-P1-003-disponibilizar-ortofoto-tenant/README.md) | Disponibilizar para Tenant | Armazena em bucket segregado |

## Fluxo Sequencial

```
Analista Drone -> UC-P1-001 -> UC-P1-002 -> UC-P1-003 -> [PARTE 2: GEOGIS]
```
