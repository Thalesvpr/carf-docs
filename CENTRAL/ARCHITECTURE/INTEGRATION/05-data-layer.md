---
type: leaf
status: review
updated: 2026-01-22
---

# Data Layer

Camada de persistencia centralizada usando PostgreSQL 15 com extensao PostGIS 3.3 para dados geoespaciais. Todos os sistemas acessam dados exclusivamente atraves da GEOAPI que implementa isolamento multi-tenant via Row-Level Security.

Schema unico contem todas as tabelas com coluna tenant_id em cada uma. RLS policies filtram automaticamente registros por tenant do usuario autenticado. Indices espaciais GiST otimizam queries geograficas. Indices B-tree em colunas de busca frequente. Particoes por tenant para tabelas de alto volume.

## PostGIS

Extensao habilita tipos geometry e geography para armazenar poligonos de unidades, pontos de interesse e linhas de limite. Funcoes ST_* validam topologia, calculam areas, detectam sobreposicoes e reprojetam coordenadas. Sistema de referencia padrao SIRGAS 2000 (EPSG:4674) com suporte a projecoes UTM por zona.
