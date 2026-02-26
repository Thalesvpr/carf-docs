---
type: standard
status: review
updated: 2026-01-22
---

# STD-001: PostgreSQL como Database

## Regra

Todo projeto que necessite de banco de dados relacional deve usar PostgreSQL 16 ou superior com extensao PostGIS 3.4 para dados geoespaciais. Nao e permitido uso de MySQL, SQLite em producao, ou bancos NoSQL como database principal.

## Justificativa

PostgreSQL com PostGIS e padrao de facto para sistemas geoespaciais governamentais brasileiros. Garante interoperabilidade com IBGE, FUNAI, ICMBio e conformidade OGC.

## Aplicacao

Aplica-se a todos os projetos do ecossistema CARF: GEOAPI, REURBWEB, REURBCAD, GEOGIS, ADMIN. Excecao: databases locais em mobile podem usar SQLite via WatermelonDB para cache offline.
