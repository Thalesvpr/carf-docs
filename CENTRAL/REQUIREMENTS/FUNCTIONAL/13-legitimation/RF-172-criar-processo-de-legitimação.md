---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-172: Criar Processo de Legitimacao

## Descricao

Sistema deve permitir criacao de processo formal de legitimacao fundiaria vinculado a unidade territorial especifica. Formulario estruturado captura dados essenciais do processo administrativo incluindo numero de protocolo, modalidade de regularizacao conforme Lei 13465/2017 (REURB-S ou REURB-E), identificacao do requerente e fundamentacao legal. Sistema estabelece vinculacao automatica entre processo e unidade territorial no banco geoespacial PostGIS, garantindo rastreabilidade bidirecional que permite consultar processos a partir de features geograficas e visualizar espacialmente unidades objeto de processos. Status inicial definido como Em Analise, iniciando workflow de tramitacao com transicoes controladas. Dados segregados por tenant_id conforme politica multi-tenant do CARF.

## Criterios de Aceitacao

1. Formulario com protocolo, modalidade REURB e requerente
2. Vinculacao a unidade territorial existente
3. Status inicial Em Analise automatico
4. Armazenamento com tenant_id
5. Validacao de dados obrigatorios

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-017, RF-044
