---
type: readme
status: review
updated: 2026-02-07
---

# INTEGRATION

Documentacao de integracao das aplicacoes CARF com o Keycloak cobrindo configuracao de clients OAuth2, gerenciamento de roles e permissoes, configuracao do realm, estrutura de tokens JWT e praticas de seguranca. Fluxo geral: usuario autentica via REURBWEB/REURBCAD/WEBDOCS/REURBMASTER com PKCE, recebe access token JWT contendo roles e claims de tenant, GEOAPI valida token como bearer-only e configura RLS no PostgreSQL via tenant_id.

A pasta organiza-se em [CLIENTS](./CLIENTS/README.md) com a configuracao dos 6 clients OAuth2 (4 public, 1 bearer-only, 1 confidential), [RBAC](./RBAC/README.md) com hierarquia de 6 roles em arvore e permissoes por endpoint, [REALM](./REALM/README.md) com settings do realm e 3 protocol mappers do scope carf-tenant, [TOKENS](./TOKENS/README.md) com estrutura JWT e ciclo de vida, e [SECURITY](./SECURITY/README.md) com hardening e protecao contra ataques.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (5)

| Pasta | Descrição |
|-------|-----------|
| [CLIENTS](./CLIENTS/README.md) | ... |
| [RBAC](./RBAC/README.md) | ... |
| [REALM](./REALM/README.md) | ... |
| [SECURITY](./SECURITY/README.md) | ... |
| [TOKENS](./TOKENS/README.md) | ... |

<!-- CARF-INDEX-END -->
