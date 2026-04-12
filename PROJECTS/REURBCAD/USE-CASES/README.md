---
type: readme
status: review
updated: 2026-02-07
---

# USE-CASES - REURBCAD

Esta secao documenta os casos de uso do aplicativo mobile REURBCAD focados na PARTE 3 do workflow mestre, que abrange a operacao em campo. Todos os casos de uso aqui descritos implementam o fluxo definido no WORKFLOW-MESTRE documentado em CENTRAL.

O fluxo sequencial da PARTE 3 inicia com a autenticacao do agente de campo via Keycloak no UC-P3-001, seguido pelo download do pacote unico e temporario no UC-P3-002, pela selecao de comunidade e carregamento do mapa no UC-P3-003, pela operacao completa em campo com GPS, formularios, assinatura e QR code no UC-P3-004, e pela sincronizacao de dados push/pull com o backend no UC-005. O REURBCAD integra-se com GEOAPI como backend que fornece pacotes e recebe sincronizacao, com GEOGIS como origem dos dados publicados na PARTE 2, e com REURBWEB como portal para visualizacao e aprovacao.

## PARTE 3: Operacao em Campo

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P3-001](./UC-P3-001-autenticar-agente-campo/README.md) | Autenticar Agente | Login via Keycloak |
| [UC-P3-002](./UC-P3-002-download-pacote-temporario/README.md) | Download Pacote | Pacote unico e temporario |
| [UC-P3-003](./UC-P3-003-selecionar-comunidade/README.md) | Selecionar Comunidade | Carregar mapa e poligonos |
| [UC-P3-004](./UC-P3-004-operar-em-campo/README.md) | Operar em Campo | GPS, formularios, assinatura, QR |
| [UC-005](./UC-005-sincronizar-dados-offline/README.md) | Sincronizar Dados | Push/pull com backend |

## Casos de Uso Complementares

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-003](./UC-003-vincular-titular-unidade/README.md) | Vincular Titular | Associar titular a unidade (pre-publicacao) |
| [UC-009](./UC-009-gerenciar-processo-legitimacao/README.md) | Legitimacao | Processo pos-workflow (fase separada) |
