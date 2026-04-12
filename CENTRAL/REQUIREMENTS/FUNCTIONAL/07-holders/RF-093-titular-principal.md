---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-093: Titular Principal

## Descricao

Sistema deve permitir marcacao de um titular como principal por unidade atraves de flag is_primary na tabela unit_holders. Titular principal representa responsavel prioritario para comunicacoes, notificacoes e apresentacao em listagens simplificadas. Validacao garante apenas um titular principal por unidade. Exibicao de unidades destaca titular principal atraves de posicionamento prioritario, formatacao diferenciada ou icone. Facilita identificacao rapida do interlocutor para questoes administrativas.

## Criterios de Aceitacao

1. Flag is_primary na tabela unit_holders
2. Apenas um titular principal por unidade
3. Destaque visual do titular principal
4. Posicionamento prioritario em listagens
5. Mudanca automatica ao marcar novo principal

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-061, RF-062
