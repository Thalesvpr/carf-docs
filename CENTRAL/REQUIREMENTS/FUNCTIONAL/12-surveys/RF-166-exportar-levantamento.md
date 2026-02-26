---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-166: Exportar Levantamento

## Descricao

Sistema deve permitir exportacao de dados de levantamento topografico em multiplos formatos tecnicos: CSV para dados tabulares de coordenadas, DXF para intercambio com softwares CAD (AutoCAD), e Shapefile para integracao com sistemas GIS desktop. Durante exportacao, sistema inclui automaticamente metadados essenciais (sistema de coordenadas, datum, data de coleta, responsavel tecnico, identificadores do projeto) garantindo rastreabilidade e conformidade com normas tecnicas. Validacao antes da geracao verifica consistencia geometrica, completude de atributos obrigatorios e integridade referencial, prevenindo exportacao de dados incompletos ou inconsistentes. Arquivos exportados mantêm estrutura compativel com especificacoes de cada formato facilitando importacao em outros sistemas.

## Criterios de Aceitacao

1. Exportacao em CSV, DXF e Shapefile
2. Inclusao automatica de metadados
3. Validacao de consistencia pre-exportacao
4. Estrutura compativel com especificacoes
5. Rastreabilidade de dados exportados

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-157, RF-141
