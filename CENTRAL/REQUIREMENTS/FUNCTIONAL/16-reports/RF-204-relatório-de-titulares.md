---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-204: Relatorio de Titulares

## Descricao

Sistema deve produzir relatorio especializado sobre titulares cadastrados apresentando estatisticas demograficas e socioeconomicas agregadas, incluindo total segmentado por tipo (pessoa fisica vs juridica), quantidades de CPF e CNPJ unicos e identificacao de titulares vinculados a multiplas unidades indicando concentracao fundiaria. Analises incluem distribuicao por genero (masculino/feminino/outros) relevante para avaliacao de equidade em programas de regularizacao, e distribuicao por faixas etarias (jovens, adultos, idosos). Estatisticas sobre tipos de relacionamento distinguem proprietarios, posseiros, cessionarios e comodatarios, alem de percentuais medios de propriedade em co-propriedade. Exportacao em Excel e PDF subsidia relatorios de impacto social. Dados filtrados por tenant_id.

## Criterios de Aceitacao

1. Segmentacao por tipo (PF/PJ)
2. Distribuicao por genero e faixa etaria
3. Estatisticas de tipos de relacionamento
4. Identificacao de multiplas unidades por titular
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-074, RF-044
