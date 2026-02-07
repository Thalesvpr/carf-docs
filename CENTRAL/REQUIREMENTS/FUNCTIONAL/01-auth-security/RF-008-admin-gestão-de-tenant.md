---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - GEOWEB
---

# RF-008: ADMIN - Gestao de Tenant

## Descricao

Usuarios com role ADMIN podem gerenciar todos recursos dentro do seu tenant especifico. Podem criar usuarios atribuindo roles (MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR), gerenciar comunidades e configurar parametros do tenant. Acesso restrito ao proprio tenant via Row Level Security baseado em claim tenant_id do JWT.

## Criterios de Aceitacao

1. ADMIN cria e gerencia usuarios do proprio tenant
2. Pode atribuir roles exceto SUPER_ADMIN e ADMIN
3. Gerencia comunidades, times e configuracoes do tenant
4. Nao visualiza dados de outros tenants
5. Dashboards gerenciais do tenant disponiveis

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB
- Requisitos dependentes: RF-006, RF-013
