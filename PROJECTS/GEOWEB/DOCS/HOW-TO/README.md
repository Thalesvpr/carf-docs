---
status: rejected
description: "Usa listas/bullets ao inves de paragrafos densos, contem listas numeradas nao convertidas para prosa"
updated: 2026-01-22
---

# HOW-TO - GEOWEB

Guias práticos para desenvolvimento e configuração do GEOWEB.

## Autenticação

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak client, redirect URIs, CORS origins, roles
- **[02-login-logout.md](./02-login-logout.md)** - Implementar login/logout buttons, useAuth hook, AuthProvider setup
- **[03-refresh-tokens.md](./03-refresh-tokens.md)** - Token refresh automático, interceptor de 401, retry failed requests

## Desenvolvimento Local

**Setup inicial:**
1. Clone do repositório
2. `npm install` ou `bun install`
3. Configurar `.env.local` com VITE_KEYCLOAK_URL e VITE_GEOAPI_URL
4. `npm run dev` para servidor de desenvolvimento

**Build para produção:**
1. `npm run build`
2. Testa build com `npm run preview`
3. Deploy para Vercel via `vercel deploy`

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/GEOWEB/DOCS/HOW-TO/01-setup-keycloak.md|01-setup-keycloak]]
- ○ [[PROJECTS/GEOWEB/DOCS/HOW-TO/02-login-logout.md|02-login-logout]]
- ○ [[PROJECTS/GEOWEB/DOCS/HOW-TO/03-refresh-tokens.md|03-refresh-tokens]]

<!-- CARF-INDEX-END -->
