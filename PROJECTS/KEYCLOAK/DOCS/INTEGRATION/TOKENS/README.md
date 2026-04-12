---
type: readme
status: review
updated: 2026-02-07
---

# TOKENS

Estrutura e ciclo de vida dos tokens JWT emitidos pelo Keycloak para autenticacao e autorizacao no ecossistema CARF. Tokens assinados com RS256, access token de 5 minutos, refresh via SSO session (idle 30min, max 10h).

O [access token](./01-access-token.md) contem claims de identidade, roles do realm e claims customizadas do scope carf-tenant (tenant_id, allowed_tenants, community_ids) para validacao em cada requisicao. O [refresh token](./02-refresh-token.md) permite renovacao silenciosa sem reautenticacao, com rotation atualmente desligada no JSON (revokeRefreshToken: false) mas recomendada pelo ADR-003 para producao. A [validacao](./03-validation.md) documenta como GEOAPI (.NET JWT Bearer) verifica assinatura, lifetime e claims, e como TenantMiddleware configura RLS no PostgreSQL.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Access Token](./01-access-token.md) | ⚠ |
| [Refresh Token](./02-refresh-token.md) | ⚠ |
| [Validação de Token](./03-validation.md) | ⚠ |

<!-- CARF-INDEX-END -->
