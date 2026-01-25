---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-162: Gerar Curvas de Nivel

## Descricao

Sistema deve gerar curvas de nivel a partir de pontos topograficos importados aplicando algoritmos de interpolacao espacial (TIN ou IDW) para estimar valores de elevacao e derivar isolinhas altimetricas. Usuario configura parametro de equidistancia vertical entre curvas conforme necessidades tecnicas (equidistancias menores para precisao, maiores para contexto regional). Curvas criadas como features LineString no banco geoespacial PostGIS preservando conectividade topologica para analises de relevo e visualizacao tridimensional. Util em projetos de regularizacao fundiaria em areas de topografia acidentada para identificar areas de risco geotecnico, planejar drenagem e validar limites de unidades conforme relevo.

## Criterios de Aceitacao

1. Interpolacao TIN ou IDW
2. Equidistancia configuravel
3. Curvas como LineString em PostGIS
4. Preservacao de conectividade topologica
5. Visualizacao no mapa

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-131
