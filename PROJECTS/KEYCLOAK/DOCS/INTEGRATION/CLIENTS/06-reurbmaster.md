---
type: leaf
status: review
updated: 2026-02-27
---

# Client REURBMASTER

Console administrativo React (Vite, porta 5174) para gestão de tenants e usuários, configurado como public client com PKCE S256.

## Configuração

| Campo | Valor |
|-------|-------|
| Client ID | `reurbmaster` |
| Tipo | Public (sem client secret) |
| Flow | Authorization Code + PKCE S256 |
| Root URL (dev) | `http://localhost:5174` |
| Redirect URIs | `http://localhost:5174/*`, `https://reurbmaster.carf.example.com/*` |
| Web Origins | `+` (same as redirect) |
| Direct Access Grants | Enabled |
| Default Client Scopes | web-origins, acr, profile, roles, email, carf-tenant |
| Browser Flow | Default (realm browser flow) |
| Direct Grant Flow | Default (realm direct grant flow) |

## Restrição de Acesso por Role

A restrição de acesso ao REURBMASTER é feita **no frontend** via `RoleGuard`:

1. **RoleGuard no router** — wrapping `<Layout />` com `allowedRoles={[SUPER_ADMIN, ADMIN, DEV]}`, bloqueia qualquer rota caso a role não bata
2. **Filtros por role em telas específicas** — ex: lista de usuários filtra por role do viewer, edit de user verifica permissão por target

> **Nota:** Um authentication flow customizado (`reurbmaster-browser`) foi criado anteriormente para restringir login no nível do Keycloak, mas causava falhas de autenticação (`invalid_user_credentials` com `User: anon`) em todas as tentativas de login no browser flow. O flow customizado foi desvinculado do client (fev/2026) e o client agora usa os flows padrão do realm. O `RoleGuard` no frontend é suficiente para impedir acesso de usuários não autorizados.

## Client Roles

| Role | Descrição |
|------|-----------|
| `manage-users` | CRUD de usuários via Admin API |
| `manage-tenants` | CRUD de tenants (prefeituras) |
| `view-audit-logs` | Acesso read-only a logs de auditoria |

## Integração com Admin API

Como o client é público (sem service account), operações na Keycloak Admin API são proxeadas via GEOAPI (backend confidential). O GEOAPI usa o client `geoapi-admin` com secret para acessar a Admin API em nome do usuário logado.
