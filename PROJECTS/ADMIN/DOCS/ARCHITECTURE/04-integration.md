# Integration - ADMIN

## Integrações

Integrações: **(1) GEOAPI** via `@carf/geoapi-client` consumindo endpoints `/api/admin/*` protegidos por role check no backend (POST /api/admin/users, DELETE /api/admin/tenants, GET /api/admin/audit-logs), GEOAPI faz proxy seguro para Keycloak Admin API mantendo client_secret confidencial no backend, **(2) @carf/tscore** para KeycloakClient gerenciando auth com PKCE flow (sem client_secret no frontend), validações (CPF, CNPJ, Email), e types compartilhados, **(3) shadcn/ui** para componentes visuais (DataTable, Dialog, Form), **(4) React Router** com protected routes validando role antes de renderizar páginas admin redirecionando para `/unauthorized` se usuário não tem permissão.

## Arquitetura de Segurança

```
ADMIN SPA (no secret)
    ↓ PKCE flow
Keycloak (auth)
    ↓ JWT
GEOAPI /api/admin/* (role check)
    ↓ client_secret (confidential)
Keycloak Admin API (gerenciamento)
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
