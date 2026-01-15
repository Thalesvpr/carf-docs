# Key Concepts - ADMIN

## Conceitos-Chave

ADMIN é console administrativo React SPA construído com Vite que consome GEOAPI `/api/admin/*` endpoints para gestão de tenants e usuários conforme arquitetura de segurança admin (ver GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md), usa PKCE flow sem `client_secret` no frontend porque Keycloak Admin API requer secret confidencial que fica isolado no backend GEOAPI fazendo proxy seguro, implementa TanStack Query para server state management com cache automático e invalidação coordenada após mutations, autorização RBAC validada em dois pontos (React Router guards no edge e role check em cada endpoint GEOAPI) seguindo onde ADMIN gerencia apenas próprio tenant e SUPER_ADMIN gerencia todos, protected routes redirecionam para login se não autenticado ou `/unauthorized` se role insuficiente, e todo fluxo é auditado no backend com logs imutáveis de quem/quando/o-quê para compliance.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
