---
type: readme
status: rejected
description: "README usa lista de bullets para descrever arquivos - reescrever em prosa densa"
updated: 2026-01-22
---

# FEATURES

Customizações Keycloak implementadas para CARF incluindo temas visuais identidade municipal, validação CPF client-side forms login, protocol mappers multi-tenancy tenant_id JWT claims, configuração realm 6 clients OAuth2 diferentes flows, e integração admin proxy GEOAPI para gestão usuários roles. Stack Keycloak 24 FreeMarker templates JavaScript validators protocol mappers User Attribute, garantindo SSO unificado entre GEOWEB REURBCAD GEOAPI GEOGIS WEBDOCS ADMIN com tokens JWT RS256 refresh automático sessões 30min idle 10h max.

## Arquivos

- **[theme-customization.md](./05-theme-customization.md)** - Tema CARF login account email FreeMarker CSS branding i18n
- **[cpf-validation.md](./03-cpf-validation.md)** - Validação CPF JavaScript client-side Mod11 User Profile
- **[multi-tenancy-claims.md](./02-multi-tenancy-claims.md)** - Claims JWT tenant_id protocol mappers RLS PostgreSQL
- **[realm-configuration.md](./01-realm-configuration.md)** - Realm CARF 6 clients roles SMTP tokens export import
- **[admin-integration.md](./04-admin-integration.md)** - Proxy GEOAPI Admin API 7 camadas CRUD users roles

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/01-realm-configuration.md|Realm Configuration - Configuração Realm]]
- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/02-multi-tenancy-claims.md|Multi-Tenancy Claims - Claims Multi-Tenancy]]
- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/03-cpf-validation.md|CPF Validation - Validação CPF]]
- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/04-admin-integration.md|Admin Integration - Integração Admin]]
- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/05-theme-customization.md|Theme Customization - Customização de Tema]]
- ○ [[PROJECTS/KEYCLOAK/DOCS/FEATURES/06-login-theme-carf.md|Login Theme CARF]]

<!-- CARF-INDEX-END -->
