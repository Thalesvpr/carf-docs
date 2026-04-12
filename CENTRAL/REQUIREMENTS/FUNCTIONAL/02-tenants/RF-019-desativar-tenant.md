---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-019: Desativar Tenant

## Descricao

Usuarios com role SUPER_ADMIN podem desativar tenant utilizando soft delete onde tenant e marcado como inativo atraves de flag is_active=false sem exclusao fisica de dados. Usuarios vinculados ao tenant desativado nao conseguem mais realizar login, recebendo mensagem especifica de tenant inativo. Dados do tenant preservados integralmente para fins de auditoria, compliance e possivel reativacao futura. Filtro global exclui automaticamente tenants inativos de listagens e queries regulares.

## Criterios de Aceitacao

1. Soft delete com flag is_active=false
2. Usuarios do tenant bloqueados de login apos desativacao
3. Mensagem especifica informando tenant inativo
4. Dados preservados para auditoria e reativacao
5. Tenants inativos excluidos de listagens padrao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-017, RF-007
