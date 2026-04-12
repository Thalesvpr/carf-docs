---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-013: Isolamento de Dados por Tenant

## Descricao

Usuarios so podem acessar dados pertencentes ao seu tenant. Implementado atraves de Row Level Security onde queries filtram automaticamente por tenant_id extraido do JWT. Tentativas de acessar tenant diferente retornam HTTP 403 Forbidden. Excecao para SUPER_ADMIN que pode trocar contexto de tenant via claim especial para administracao cross-tenant.

## Criterios de Aceitacao

1. Todas queries filtram por tenant_id automaticamente
2. Manipulacao de parametros para outro tenant retorna 403
3. RLS aplicado em nivel de banco de dados
4. SUPER_ADMIN pode acessar qualquer tenant
5. Logs registram acessos cross-tenant de SUPER_ADMIN

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-005, RF-006
