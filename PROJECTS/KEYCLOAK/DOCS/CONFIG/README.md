---
type: readme
status: review
updated: 2026-02-07
---

# CONFIG

Arquivos de configuracao para deploy e desenvolvimento do Keycloak no ambiente CARF. O realm-export.json nesta pasta e um redirect — a fonte da verdade esta em CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json.

O [docker-compose.yml](./docker-compose.yml) sobe Keycloak 24 com PostgreSQL 16 em rede carf-network, importando o realm via --import-realm. O [realm-export.json](./realm-export.json) redireciona para o arquivo real em CENTRAL contendo 6 clients, 6 roles com composites, scope carf-tenant com 3 mappers (tenant_id, allowed_tenants, community_ids) e brute force protection. O [.env.example](./.env.example) documenta todas variaveis de ambiente necessarias (KC_DB, KC_HOSTNAME, KEYCLOAK_ADMIN, etc).

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

<!-- CARF-INDEX-END -->
