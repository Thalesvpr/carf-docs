---
type: leaf
status: approved
updated: 2026-02-21
---

# GEOAPI

Backend REST API central do ecossistema CARF construido em .NET 9 que serve como unico ponto de entrada para todos os clientes. Recebe ortofotos do Operador de Drone, processa e reduz tamanho, armazenando em bucket S3/MinIO segregado por tenant. Expoe endpoints para gestao de unidades habitacionais, titulares, comunidades, processos de legitimacao e documentos. Processa dados geoespaciais usando PostGIS e implementa regras de negocio do dominio REURB.

Todos os sistemas consomem GEOAPI via HTTP autenticado. REURBWEB usa para interface de analistas. REURBCAD sincroniza dados coletados em campo. REURBMASTER gerencia tenants e usuarios. GEOGIS acessa dados via WFS. Autenticacao via JWT tokens do Keycloak com isolamento multi-tenant por Row-Level Security no PostgreSQL.

## Capacidades

API REST documentada com OpenAPI/Swagger. Validacao topologica e calculo de areas com PostGIS. Sincronizacao offline processando batches do mobile. Geracao de relatorios PDF/Excel. Servicos WFS para clientes GIS. Webhooks para eventos de negocio. Detalhes tecnicos no repositorio carf-geoapi.
