---
type: readme
status: review
updated: 2026-02-07
---

# REALM

Configuracao do realm CARF no Keycloak incluindo settings gerais de sessao e tokens, protocol mappers para claims customizados e configuracao de temas visuais.

A [configuracao](./01-configuration.md) documenta settings do realm como lifetimes (access token 5min, SSO idle 30min, SSO max 10h, offline 30d), brute force protection (5 tentativas, lockout progressivo) e password policy length(8). Os [protocol mappers](./02-protocol-mappers.md) explicam como atributos de usuario sao mapeados para claims JWT via scope carf-tenant: tenant_id (String, current_tenant), allowed_tenants (JSON multivalued, tenants) e community_ids (JSON multivalued). A [configuracao de tema](./03-theme-configuration.md) cobre como ativar e gerenciar o tema CARF nas paginas de login, account e email.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Configuração do Realm](./01-configuration.md) | ⚠ |
| [Protocol Mappers](./02-protocol-mappers.md) | ⚠ |
| [Configuração de Tema no Realm](./03-theme-configuration.md) | ⚠ |

<!-- CARF-INDEX-END -->
