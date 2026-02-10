---
type: leaf
status: review
updated: 2026-02-08
---

# ICurrentUser

Interface fornecendo dados do usuario autenticado atual extraidos de JWT token, permitindo acesso a AccountId, TenantId, Role e claims sem depender diretamente de HttpContext. Mantem domain e application layers independentes de infraestrutura web.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| AccountId | (propriedade) | Guid | UUID do usuario autenticado (claim sub). |
| TenantId | (propriedade) | Guid | Tenant atual (claim tenant_id). |
| Email | (propriedade) | string | Email do usuario. |
| Name | (propriedade) | string | Nome completo. |
| Role | (propriedade) | Role | Papel: SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR. |
| IsAuthenticated | (propriedade) | bool | Se usuario esta autenticado. |
| HasRole | Role role | bool | Verifica papel especifico. |
| HasPermission | string permission | bool | Verifica permissao granular. |

Implementada por HttpCurrentUser extraindo claims de HttpContext, e por BackgroundJobCurrentUser em jobs. Usada em command handlers para validar permissoes, em audit logging, e em domain services para verificar ownership.
