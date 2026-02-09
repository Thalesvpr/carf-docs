---
type: leaf
status: review
updated: 2026-02-07
---

# Environment Variables

Configuracao do Keycloak via environment variables para containerizacao. Todas variaveis seguem prefixo KC_ para Quarkus-based Keycloak (v17+).

## Credenciais de Admin

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KEYCLOAK_ADMIN | Username do admin inicial | - |
| KEYCLOAK_ADMIN_PASSWORD | Senha do admin inicial | - |

Credenciais so sao usadas na primeira inicializacao. Apos criar o admin, remover por seguranca.

## Database

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_DB | Tipo do banco | dev-file |
| KC_DB_URL | JDBC connection string | - |
| KC_DB_URL_HOST | Host do banco | - |
| KC_DB_URL_PORT | Porta do banco | 5432 |
| KC_DB_URL_DATABASE | Nome do banco | keycloak |
| KC_DB_USERNAME | Usuario do banco | - |
| KC_DB_PASSWORD | Senha do banco | - |
| KC_DB_SCHEMA | Schema PostgreSQL | public |
| KC_DB_POOL_INITIAL_SIZE | Pool inicial | 0 |
| KC_DB_POOL_MIN_SIZE | Pool minimo | 0 |
| KC_DB_POOL_MAX_SIZE | Pool maximo | 100 |

## Hostname e HTTPS

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_HOSTNAME | Hostname publico | - |
| KC_HOSTNAME_ADMIN | Hostname do admin console | igual KC_HOSTNAME |
| KC_HOSTNAME_STRICT | Rejeita requests de outros hosts | true |
| KC_HOSTNAME_STRICT_HTTPS | Forca HTTPS | true |
| KC_HOSTNAME_STRICT_BACKCHANNEL | Strict para backchannel | false |

Em producao, STRICT e STRICT_HTTPS devem ser true. Em desenvolvimento, ambos false com hostname localhost.

Ver [05a-environment-variables-ops](./05a-environment-variables-ops.md) para HTTP, proxy, health, logging, cache e temas.
