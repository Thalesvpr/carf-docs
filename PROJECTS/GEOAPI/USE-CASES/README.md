---
type: readme
status: review
updated: 2026-02-21
---

# USE-CASES - GEOAPI

Esta secao documenta os casos de uso do backend GEOAPI focados na PARTE 1 do workflow mestre, que abrange o recebimento e processamento de ortofotos. Todos os casos de uso aqui descritos implementam o fluxo definido no WORKFLOW-MESTRE documentado em CENTRAL.

O fluxo sequencial da PARTE 1 inicia com o Operador de Drone entregando a ortofoto via UC-P1-001, seguido pelo processamento e otimizacao automatica no backend via UC-P1-002, e finaliza com o armazenamento em bucket segregado por tenant via UC-P1-003. Ao concluir esta parte, os dados ficam disponiveis para a PARTE 2 executada pelo GEOGIS.

## PARTE 1: Entrega e Processamento de Ortofotos

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P1-001](./UC-P1-001-entregar-ortofoto/README.md) | Entregar Ortofoto | Operador de Drone envia ortofoto |
| [UC-P1-002](./UC-P1-002-processar-ortofoto/README.md) | Processar Ortofoto | Backend processa e otimiza |
| [UC-P1-003](./UC-P1-003-disponibilizar-ortofoto-tenant/README.md) | Disponibilizar para Tenant | Armazena em bucket segregado |
