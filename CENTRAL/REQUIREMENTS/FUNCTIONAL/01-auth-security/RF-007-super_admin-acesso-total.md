---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - REURBWEB
---

# RF-007: SUPER_ADMIN - Acesso Total

## Descricao

Usuarios com role SUPER_ADMIN devem ter acesso irrestrito a todas funcionalidades e recursos do sistema transcendendo limitacoes de tenant. Podem criar, editar e excluir qualquer recurso em qualquer tenant. Claim especial no JWT permite que queries ignorem filtros automaticos de tenant_id. Acesso a configuracoes globais de sistema, integracoes externas e politicas de seguranca.

## Criterios de Aceitacao

1. SUPER_ADMIN acessa recursos de qualquer tenant
2. Queries de banco ignoram filtro RLS para esta role
3. Interface administrativa global acessivel
4. Pode gerenciar configuracoes de infraestrutura
5. Auditoria registra todas acoes cross-tenant

## Rastreabilidade

- Modulos: GEOAPI, REURBWEB
- Requisitos dependentes: RF-006, RF-013
