---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - REURBCAD
---

# RF-065: Buscar Unidade por Localizacao

## Descricao

Sistema deve oferecer endpoint de busca espacial de unidades atraves de coordenadas geograficas e raio de distancia. API GEOAPI recebe parametros lat, lon e radius (metros) retornando unidades dentro da area circular especificada. Implementacao utiliza indices espaciais do PostGIS com operadores geometricos nativos garantindo performance otimizada. Resultados ordenados por distancia crescente do ponto de consulta. Recurso essencial para aplicativo REURBCAD onde agentes localizam unidades proximas a sua posicao atual conforme WORKFLOW-MESTRE.

## Criterios de Aceitacao

1. Endpoint com parametros lat, lon, radius
2. Busca espacial via PostGIS com indices
3. Ordenacao por distancia crescente
4. Performance otimizada para grandes volumes
5. Resposta com distancia de cada unidade

## Rastreabilidade

- Modulos: GEOAPI, REURBCAD
- Requisitos dependentes: RF-052, RF-066
