---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-139: Importar Shapefile em Camada

## Descricao

Sistema deve permitir importacao de shapefiles ESRI em camadas existentes criando features automaticamente a partir dos dados geoespaciais contidos. Upload aceita arquivo ZIP contendo componentes obrigatorios (.shp, .shx, .dbf) e opcionalmente .prj para sistema de coordenadas, com validacao de presenca de todos arquivos necessarios. Funcionalidade de mapeamento de atributos permite especificar correspondencia entre campos do DBF e schema de atributos customizados da camada destino, incluindo renomeacao, conversao de tipos e omissao de campos. Importacao em lote via transacao unica le geometrias e atributos, valida cada feature conforme tipo da camada e insere registros com feedback de progresso e relatorio final de sucessos e erros. Sistema reprojeta geometrias se necessario convertendo do sistema de coordenadas do shapefile para SRID configurado.

## Criterios de Aceitacao

1. Upload de ZIP com componentes shapefile
2. Mapeamento de atributos DBF para schema
3. Importacao em lote com transacao unica
4. Feedback de progresso e relatorio final
5. Reprojecao automatica de coordenadas

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-132, RF-136
