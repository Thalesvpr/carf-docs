---
type: adr
status: review
updated: 2026-01-22
---

# ADR-001: Row-Level Security para Multi-Tenancy

## Contexto

Sistema CARF atende multiplos municipios com dados completamente isolados. Cada prefeitura deve acessar apenas seus registros. A estrategia de isolamento impacta seguranca, complexidade de queries e custos de infraestrutura. Decisao necessaria antes de definir schema do banco.

## Decisao

Adotamos Row-Level Security do PostgreSQL com schema unico compartilhado. Todas as tabelas possuem coluna tenant_id e policies RLS filtram automaticamente por tenant do usuario autenticado. GEOAPI configura contexto de tenant via SET LOCAL no inicio de cada requisicao.

## Consequencias

Simplifica operacoes com banco unico para backup, migracao e monitoramento. Permite queries cross-tenant para relatorios administrativos desabilitando RLS temporariamente. Risco de vazamento se policy mal configurada. Indices compostos com tenant_id aumentam tamanho mas garantem performance.

## Alternativas Rejeitadas

Schema por tenant foi descartado por complexidade operacional com centenas de municipios e dificuldade de atualizacoes de schema. Banco separado por tenant foi rejeitado por custo de infraestrutura e impossibilidade de analises agregadas. Filtro em application layer foi descartado por risco de esquecimento em queries.
