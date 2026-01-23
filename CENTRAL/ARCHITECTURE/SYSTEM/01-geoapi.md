---
type: leaf
status: review
updated: 2026-01-22
---

# GEOAPI

Backend REST API central do ecossistema CARF construido em .NET 9 que serve como unico ponto de entrada para todos os clientes. Expoe endpoints para gestao de unidades habitacionais, titulares, comunidades, processos de legitimacao e documentos. Processa dados geoespaciais usando PostGIS e implementa regras de negocio do dominio REURB.

Todos os sistemas consomem GEOAPI via HTTP autenticado. GEOWEB usa para interface de analistas. REURBCAD sincroniza dados coletados em campo. ADMIN gerencia tenants e usuarios. GEOGIS acessa dados via WFS. Autenticacao via JWT tokens do Keycloak com isolamento multi-tenant por Row-Level Security no PostgreSQL.

## Capacidades

API REST documentada com OpenAPI/Swagger. Validacao topologica e calculo de areas com PostGIS. Sincronizacao offline processando batches do mobile. Geracao de relatorios PDF/Excel. Servicos WFS para clientes GIS. Webhooks para eventos de negocio. Detalhes tecnicos em [PROJECTS/GEOAPI/DOCS/](../../../PROJECTS/GEOAPI/DOCS/README.md).
