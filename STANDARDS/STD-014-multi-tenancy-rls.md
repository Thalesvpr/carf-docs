---
type: standard
status: review
updated: 2026-01-22
---

# STD-014: Multi-tenancy via RLS

## Regra

Isolamento de dados entre tenants deve usar Row-Level Security nativo do PostgreSQL. Proibido database-per-tenant, schema-per-tenant, ou filtragem apenas em application layer.

## Justificativa

RLS garante isolamento no database layer, imune a bugs de codigo. Single database simplifica operacao. Policies auditaveis facilitam compliance LGPD.

## Aplicacao

Todas tabelas multi-tenant em GEOAPI: units, holders, communities, processes, documents. Session variable tenant_id extraida do JWT Keycloak.
