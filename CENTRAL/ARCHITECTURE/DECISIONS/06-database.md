---
type: adr
status: current
updated: 2026-01-22
---

# ADR-006: PostgreSQL com PostGIS

## Contexto

Sistema armazena geometrias de unidades, comunidades e camadas vetoriais. Operacoes espaciais como intersecao, buffer e validacao de sobreposicao sao requisitos criticos. Escolha de banco impacta performance de queries espaciais e compatibilidade com ferramentas GIS padrao de mercado.

## Decisao

Adotamos PostgreSQL 15 com extensao PostGIS 3.3. Tipos nativos geometry e geography armazenam poligonos e pontos. Indices GiST aceleram queries espaciais. Funcoes ST conformes com OGC Simple Features. SIRGAS 2000 como sistema de referencia padrao.

## Consequencias

Performance excelente em queries espaciais complexas. Compatibilidade direta com QGIS, GeoServer e outras ferramentas GIS. Comunidade ativa e documentacao extensa. Requer conhecimento de SQL espacial para queries avancadas. Backup e restore mais complexos que bancos convencionais.

## Alternativas Rejeitadas

MongoDB geospatial foi descartado por limitacoes em operacoes complexas como dissolve e union. SQL Server Spatial foi rejeitado por custo de licenciamento e menor ecossistema GIS. Armazenar GeoJSON como texto foi descartado por impossibilitar indices espaciais.
