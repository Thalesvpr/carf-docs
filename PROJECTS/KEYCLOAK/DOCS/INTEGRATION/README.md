---
type: readme
status: rejected
description: "Usa tabelas e diagrama ASCII ao inves de prosa densa - reescrever em paragrafos"
updated: 2026-01-22
---

# INTEGRATION

Documentacao de integracao das aplicacoes CARF com o Keycloak, cobrindo configuracao de clients OAuth2, gerenciamento de roles e permissoes, configuracao do realm, estrutura de tokens JWT e praticas de seguranca.

## Estrutura

| Pasta | Conteudo |
|:------|:---------|
| [CLIENTS](./CLIENTS/README.md) | Configuracao dos 6 clients OAuth2 (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN) |
| [RBAC](./RBAC/README.md) | Hierarquia de roles e mapeamento de permissoes |
| [REALM](./REALM/README.md) | Configuracao do realm CARF, protocol mappers e temas |
| [TOKENS](./TOKENS/README.md) | Estrutura de access/refresh tokens JWT e validacao |
| [SECURITY](./SECURITY/README.md) | Boas praticas, protecao contra ataques e secrets |

## Fluxo de Autenticacao

```
Usuario → GEOWEB/REURBCAD/WEBDOCS/ADMIN
           ↓
      Keycloak (PKCE)
           ↓
      Access Token JWT
           ↓
      GEOAPI (Bearer Validation)
           ↓
      PostgreSQL (RLS by tenant_id)
```


