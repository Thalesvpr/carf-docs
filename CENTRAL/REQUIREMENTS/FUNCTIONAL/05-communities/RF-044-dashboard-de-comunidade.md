---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-044: Dashboard de Comunidade

## Descricao

Interface deve apresentar visualizacao consolidada de metricas e graficos especificos da comunidade. Graficos de status de unidades exibem distribuicao por workflow state utilizando graficos de pizza ou barras com cores distintas por status. Mapa de calor de densidade mostra concentracao espacial de unidades dentro do boundary. Indicadores numericos exibem KPIs essenciais em cards destacados incluindo total de unidades, titulares, area e taxa de aprovacao.

## Criterios de Aceitacao

1. Graficos de distribuicao por status de unidades
2. Mapa de calor de densidade espacial
3. Cards com KPIs essenciais
4. Atualizacao near-real-time
5. Queries otimizadas com caching

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-041, RF-038
