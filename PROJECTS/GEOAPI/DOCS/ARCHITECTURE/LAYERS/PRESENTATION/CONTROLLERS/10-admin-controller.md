---
type: leaf
status: review
updated: 2026-02-08
---

# Admin Controller

O AdminController serve como proxy seguro para a Keycloak Admin API, permitindo que o console REURBMASTER gerencie usuarios, roles e tenants sem expor client_secret no frontend. A rota base e /api/admin. Todos os endpoints requerem role admin ou super-admin. O backend utiliza Keycloak Admin Client com client credentials flow para comunicar com a Admin API do Keycloak.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/admin/tenants | Listar tenants | 200 | - | super-admin |
| POST | /api/admin/tenants | Criar tenant | 201 | 400 | super-admin |
| GET | /api/admin/users | Listar usuarios do tenant | 200 | - | admin+ |
| POST | /api/admin/users | Criar usuario | 201 | 400, 409 | admin+ |
| PUT | /api/admin/users/{id} | Atualizar usuario | 200 | 404 | admin+ |
| DELETE | /api/admin/users/{id} | Desativar usuario | 204 | 404 | admin+ |
| GET | /api/admin/users/{id}/roles | Listar roles do usuario | 200 | 404 | admin+ |
| POST | /api/admin/users/{id}/roles | Atribuir roles | 200 | 404 | admin+ |
| DELETE | /api/admin/users/{id}/roles | Remover roles | 204 | 404 | admin+ |
| GET | /api/admin/audit-logs | Consultar logs auditoria | 200 | - | admin+ |

## Comportamento

Todas as operacoes de gerenciamento de usuarios sao delegadas ao KeycloakAdminService que utiliza client_secret confidencial armazenado no backend para comunicar com a Keycloak Admin REST API. O admin com role admin pode gerenciar apenas usuarios do proprio tenant, filtrado via tenant_id do JWT. O super-admin pode gerenciar usuarios de qualquer tenant e criar novos tenants. O endpoint de audit-logs consulta a tabela audit_logs do PostgreSQL com filtros por entityType, entityId, userId, startDate e endDate, suportando paginacao padrao.

## Autorizacao

Endpoints de tenants requerem exclusivamente role super-admin. Endpoints de usuarios e roles requerem admin ou super-admin, com restricao de escopo por tenant para admin. Logs de auditoria sao acessiveis por admin ou superior. As 7 camadas de seguranca incluem autenticacao JWT, autorizacao RBAC, isolamento por tenant, validacao de entrada, rate limiting, auditoria e criptografia TLS.
