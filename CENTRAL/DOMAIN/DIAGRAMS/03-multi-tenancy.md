---
type: leaf
status: approved
updated: 2026-02-07
---

# Multi-Tenancy Diagram

Descricao do fluxo de isolamento multi-tenant via JWT e Row-Level Security no PostgreSQL, demonstrando as camadas de seguranca defense-in-depth.

## Fluxo de Isolamento

O usuario envia requisicao HTTP ao GEOAPI. O controller encaminha ao middleware de validacao JWT, que extrai os claims do token: sub (user_id), email, roles e tenant_id. O middleware configura o EF Core DbContext com o tenant extraido. O DbContext define a session variable no PostgreSQL via SET app.current_tenant.

Quando uma query SQL e executada (por exemplo, buscar unidades aprovadas), a policy RLS units_tenant_isolation intercepta automaticamente e adiciona o filtro tenant_id igual ao current_setting. O resultado retorna apenas linhas do tenant correto, garantindo isolamento completo.

## Etapas do Fluxo

| Etapa | Componente | Acao |
|-------|-----------|------|
| 1 | GEOAPI Controller | Recebe requisicao HTTP com JWT |
| 2 | JWT Validation Middleware | Valida token e extrai claims |
| 3 | EF Core DbContext | Recebe tenant_id dos claims |
| 4 | PostgreSQL Session Variable | Define app.current_tenant via SET |
| 5 | SQL Query | Executa query original sem filtro de tenant |
| 6 | RLS Policy | Intercepta e adiciona filtro automatico por tenant_id |
| 7 | Query Filtrada | Retorna apenas linhas do tenant correto |

## Camadas de Seguranca

| Camada | Mecanismo | Descricao |
|--------|-----------|-----------|
| Camada 1 | Middleware JWT | Valida token e extrai tenant_id do claim |
| Camada 2 | PostgreSQL RLS | Aplica filtro automatico no kernel do banco |

Arquitetura defense-in-depth com duas camadas de protecao. Middleware valida token JWT e extrai tenant_id dos claims. PostgreSQL RLS aplica filtro automatico em todas as queries, impossibilitando vazamento de dados entre tenants mesmo em caso de SQL injection.
