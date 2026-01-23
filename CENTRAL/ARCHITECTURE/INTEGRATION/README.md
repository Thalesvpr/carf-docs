---
type: readme
status: current
updated: 2026-01-22
---

# INTEGRATION

Documentacao de como os sistemas do ecossistema CARF se comunicam entre si, definindo padroes de integracao, protocolos utilizados e fluxos de dados entre componentes.

A [autenticacao](./01-authentication.md) documenta como todos os sistemas se autenticam via Keycloak usando OAuth2/OIDC, incluindo fluxos Authorization Code com PKCE para aplicacoes web e mobile, e Client Credentials para comunicacao backend-to-backend. A [comunicacao via API](./02-api-communication.md) especifica como clientes consomem a GEOAPI usando REST, JWT bearer tokens e headers de tenant para isolamento multi-tenant.

A [sincronizacao offline](./03-offline-sync.md) detalha como o REURBCAD sincroniza dados coletados em campo com o backend, incluindo estrategia de resolucao de conflitos, priorizacao de uploads e gerenciamento de fila. As [bibliotecas compartilhadas](./04-shared-libraries.md) documentam os pacotes @carf/tscore, @carf/ui e geoapi-client que promovem reuso de codigo entre projetos frontend. A [camada de dados](./05-data-layer.md) explica como PostgreSQL com PostGIS e Row-Level Security fornece persistencia e isolamento para todos os sistemas.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (5)

| Documento | Status |
|-----------|--------|
| [Authentication](./01-authentication.md) | ⚠ |
| [API Communication](./02-api-communication.md) | ⚠ |
| [Offline Sync](./03-offline-sync.md) | ⚠ |
| [Shared Libraries](./04-shared-libraries.md) | ⚠ |
| [Data Layer](./05-data-layer.md) | ⚠ |

<!-- CARF-INDEX-END -->
