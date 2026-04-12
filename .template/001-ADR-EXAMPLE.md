---
type: adr
status: review
updated: 2026-01-22
---

# ADR-001: PostgreSQL com PostGIS para Dados Geoespaciais

## Contexto

O sistema CARF precisa armazenar e consultar geometrias de unidades habitacionais, comunidades e camadas vetoriais. Operacoes espaciais como intersecao, buffer e validacao de sobreposicao sao requisitos funcionais criticos. A escolha do banco impacta performance de queries espaciais e compatibilidade com ferramentas GIS.

## Decisao

Adotamos PostgreSQL com extensao PostGIS como banco de dados principal. PostGIS oferece tipos nativos de geometria, indices espaciais R-tree via GiST, e funcoes SQL padrao OGC. A integracao com Entity Framework Core via Npgsql.EntityFrameworkCore.PostgreSQL.NetTopologySuite permite mapeamento direto de geometrias para entidades de dominio.

## Consequencias

Melhora a performance de queries espaciais com indices especializados. Simplifica codigo ao usar tipos nativos ao inves de serializar geometrias. Aumenta dependencia de infraestrutura especifica, dificultando migracao futura para outros bancos. Requer conhecimento de SQL espacial para queries complexas.

## Alternativas Rejeitadas

MongoDB com suporte geoespacial foi descartado por limitacoes em operacoes complexas como ST_Union e ST_Difference. SQL Server Spatial foi rejeitado por custo de licenciamento e menor ecossistema de ferramentas GIS. Armazenar geometrias como GeoJSON em campo texto foi descartado por impossibilitar indices espaciais.
