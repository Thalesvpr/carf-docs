---
id: RNF-003
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-003: Tempo de Resposta - Queries Espaciais

## Descricao

Buscas espaciais do GEOAPI (bbox, radius) devem responder em tempo aceitavel considerando calculos geometricos complexos. Aplica-se a endpoints como GET /api/units/search-area e GET /api/units/search-radius.

## Metricas

- Tempo de resposta: <= 2000ms no percentil 95
- Condicoes: carga normal de operacao com indices espaciais ativos
- Ferramenta de medicao: k6 ou Artillery

## Criterios de Aceitacao

1. 95% das queries espaciais completam em ate 2 segundos
2. Indices espaciais PostGIS GIST implementados nas colunas de geometria
3. Testes de carga validam metrica sob cenario realista
