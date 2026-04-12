---
type: readme
status: review
updated: 2026-02-07
---

# FEATURES

Customizacoes Keycloak implementadas para o CARF garantindo SSO unificado entre REURBWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS e ADMIN com tokens JWT RS256 contendo claims de tenant e roles. Stack Keycloak 24 com temas FreeMarker (migracao Keycloakify planejada via ADR-001), protocol mappers do scope carf-tenant e configuracao de 6 clients OAuth2.

A [realm-configuration](./01-realm-configuration.md) documenta o realm CARF com 6 clients, registration OFF, verifyEmail OFF e password policy length(8). O [multi-tenancy-claims](./02-multi-tenancy-claims.md) explica protocol mappers tenant_id, allowed_tenants e community_ids. A [cpf-validation](./03-cpf-validation.md) cobre validacao CPF client-side via JavaScript Mod11. A [admin-integration](./04-admin-integration.md) documenta proxy da Admin API via GEOAPI. O [theme-customization](./05-theme-customization.md) e [login-theme-carf](./06-login-theme-carf.md) cobrem o tema visual CARF com branding, i18n pt-BR/en e FreeMarker CSS.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (6)

| Documento | Status |
|-----------|--------|
| [Realm Configuration - Configuração Realm](./01-realm-configuration.md) | ⚠ |
| [Multi-Tenancy Claims - Claims Multi-Tenancy](./02-multi-tenancy-claims.md) | ⚠ |
| [CPF Validation - Validação CPF](./03-cpf-validation.md) | ⚠ |
| [Admin Integration - Integração Admin](./04-admin-integration.md) | ⚠ |
| [Theme Customization - Customização de Tema](./05-theme-customization.md) | ⚠ |
| [Login Theme CARF](./06-login-theme-carf.md) | ⚠ |

<!-- CARF-INDEX-END -->
