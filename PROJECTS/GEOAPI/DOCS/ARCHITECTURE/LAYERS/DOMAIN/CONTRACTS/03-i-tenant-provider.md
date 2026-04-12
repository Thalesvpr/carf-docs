---
type: leaf
status: review
updated: 2026-02-08
---

# ITenantProvider

Interface fornecendo TenantId do contexto atual da requisicao, extraido de JWT token ou header, permitindo isolamento de dados por cliente atraves de Row-Level Security (RLS) sem passar TenantId manualmente em cada operacao.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| GetTenantId | (nenhum) | Guid | Retorna tenant atual. Lanca exception se fora de contexto autenticado. |
| HasTenant | (nenhum) | bool | Verifica se contexto tem tenant disponivel. |

Implementada por HttpTenantProvider extraindo tenant_id de claim JWT, e por BackgroundJobTenantProvider em jobs agendados. Usada em repositories (global query filter), command handlers (popular TenantId em entidades), e audit logs. Integra com RLS do PostgreSQL via session variable app.current_tenant.
