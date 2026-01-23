---
type: standard
status: approved
updated: 2026-01-22
---

# STD-010: PostgreSQL como Database

## Regra

Todo projeto que necessite banco relacional deve usar PostgreSQL 16+ com PostGIS 3.4 para dados geoespaciais. Proibido MySQL, MariaDB, SQLite em producao, ou NoSQL como database principal.

## Justificativa

PostgreSQL com PostGIS e padrao para sistemas geoespaciais governamentais brasileiros. Garante interoperabilidade com IBGE, FUNAI, ICMBio. RLS nativo permite multi-tenancy seguro.

## Aplicacao

Todos os projetos CARF: GEOAPI, GEOWEB, REURBCAD, GEOGIS, ADMIN. Excecao: mobile usa SQLite local via WatermelonDB para cache offline.
