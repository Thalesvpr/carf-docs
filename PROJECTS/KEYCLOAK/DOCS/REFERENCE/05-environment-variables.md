---
status: review
updated: 2026-01-21
---

# Environment Variables

Configuração do Keycloak via environment variables para containerização seguindo twelve-factor app principles. Todas variáveis seguem o prefixo `KC_` para o Quarkus-based Keycloak (v17+).

## Credenciais de Admin

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KEYCLOAK_ADMIN` | Username do admin inicial | - | `admin` |
| `KEYCLOAK_ADMIN_PASSWORD` | Senha do admin inicial | - | `<senha-forte>` |

```yaml
environment:
  KEYCLOAK_ADMIN: admin
  KEYCLOAK_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}  # Via secrets
```

**Nota**: Credenciais de admin só são usadas na primeira inicialização. Após criar o usuário admin, recomenda-se remover essas variáveis por segurança.

## Database

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_DB` | Tipo do banco de dados | `dev-file` | `postgres` |
| `KC_DB_URL` | JDBC connection string | - | `jdbc:postgresql://db:5432/keycloak` |
| `KC_DB_URL_HOST` | Host do banco (alternativa) | - | `db` |
| `KC_DB_URL_PORT` | Porta do banco | `5432` | `5432` |
| `KC_DB_URL_DATABASE` | Nome do banco | `keycloak` | `keycloak` |
| `KC_DB_USERNAME` | Usuário do banco | - | `keycloak` |
| `KC_DB_PASSWORD` | Senha do banco | - | `<senha>` |
| `KC_DB_SCHEMA` | Schema (PostgreSQL) | `public` | `keycloak` |
| `KC_DB_POOL_INITIAL_SIZE` | Tamanho inicial do pool | `0` | `5` |
| `KC_DB_POOL_MIN_SIZE` | Tamanho mínimo do pool | `0` | `5` |
| `KC_DB_POOL_MAX_SIZE` | Tamanho máximo do pool | `100` | `20` |

```yaml
environment:
  KC_DB: postgres
  KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
  KC_DB_USERNAME: keycloak
  KC_DB_PASSWORD: ${KC_DB_PASSWORD}
  KC_DB_POOL_MIN_SIZE: 5
  KC_DB_POOL_MAX_SIZE: 20
```

## Hostname e HTTPS

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_HOSTNAME` | Hostname público | - | `keycloak.carf.gov.br` |
| `KC_HOSTNAME_ADMIN` | Hostname do admin console | (igual KC_HOSTNAME) | `admin.keycloak.carf.gov.br` |
| `KC_HOSTNAME_STRICT` | Rejeita requests de outros hosts | `true` | `true` |
| `KC_HOSTNAME_STRICT_HTTPS` | Força HTTPS | `true` | `true` |
| `KC_HOSTNAME_STRICT_BACKCHANNEL` | Strict para backchannel | `false` | `false` |

```yaml
# Produção com domínio público
environment:
  KC_HOSTNAME: keycloak.carf.gov.br
  KC_HOSTNAME_STRICT: true
  KC_HOSTNAME_STRICT_HTTPS: true

# Desenvolvimento local
environment:
  KC_HOSTNAME: localhost
  KC_HOSTNAME_STRICT: false
  KC_HOSTNAME_STRICT_HTTPS: false
```

## HTTP/HTTPS

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_HTTP_ENABLED` | Habilita HTTP (porta 8080) | `false` (prod) | `true` |
| `KC_HTTP_PORT` | Porta HTTP | `8080` | `8080` |
| `KC_HTTP_RELATIVE_PATH` | Path base | `/` | `/auth` |
| `KC_HTTPS_PORT` | Porta HTTPS | `8443` | `8443` |
| `KC_HTTPS_CERTIFICATE_FILE` | Caminho do certificado | - | `/certs/tls.crt` |
| `KC_HTTPS_CERTIFICATE_KEY_FILE` | Caminho da chave privada | - | `/certs/tls.key` |
| `KC_HTTPS_KEY_STORE_FILE` | Keystore JKS | - | `/certs/keystore.jks` |
| `KC_HTTPS_KEY_STORE_PASSWORD` | Senha do keystore | - | `<senha>` |

```yaml
# Produção com certificado TLS
environment:
  KC_HTTP_ENABLED: false
  KC_HTTPS_PORT: 8443
  KC_HTTPS_CERTIFICATE_FILE: /certs/tls.crt
  KC_HTTPS_CERTIFICATE_KEY_FILE: /certs/tls.key

# Desenvolvimento (HTTP enabled)
environment:
  KC_HTTP_ENABLED: true
  KC_HTTP_PORT: 8080
```

## Proxy e Load Balancer

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_PROXY` | Modo de proxy | `none` | `edge` |

**Valores de KC_PROXY:**
- `none` - Sem proxy
- `edge` - Proxy termina TLS (mais comum)
- `reencrypt` - Proxy termina TLS e re-encrypta para Keycloak
- `passthrough` - TLS pass-through para Keycloak

```yaml
# Atrás de nginx/traefik que termina TLS
environment:
  KC_PROXY: edge
  KC_HOSTNAME: keycloak.carf.gov.br
  KC_HTTP_ENABLED: true  # Proxy conecta via HTTP
```

## Health e Metrics

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_HEALTH_ENABLED` | Habilita /health endpoints | `false` | `true` |
| `KC_METRICS_ENABLED` | Habilita /metrics Prometheus | `false` | `true` |

```yaml
environment:
  KC_HEALTH_ENABLED: true
  KC_METRICS_ENABLED: true
```

**Endpoints:**
- `/health` - Status geral
- `/health/live` - Liveness probe (Kubernetes)
- `/health/ready` - Readiness probe (Kubernetes)
- `/metrics` - Métricas Prometheus

## Logging

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_LOG_LEVEL` | Nível de log | `info` | `warn` |
| `KC_LOG` | Formato de output | `console` | `console,file` |
| `KC_LOG_CONSOLE_FORMAT` | Formato console | `default` | `json` |
| `KC_LOG_FILE` | Path do arquivo de log | - | `/logs/keycloak.log` |

```yaml
# Produção com logs JSON
environment:
  KC_LOG_LEVEL: warn
  KC_LOG: console
  KC_LOG_CONSOLE_FORMAT: json

# Desenvolvimento verbose
environment:
  KC_LOG_LEVEL: debug
  KC_LOG: console
```

## Cache e Clustering

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_CACHE` | Tipo de cache | `ispn` | `local` |
| `KC_CACHE_STACK` | Stack de rede para cluster | - | `tcp` |
| `KC_CACHE_CONFIG_FILE` | Arquivo de config Infinispan | - | `/cache/cache-ispn.xml` |

```yaml
# Single node (dev)
environment:
  KC_CACHE: local

# Cluster com TCP
environment:
  KC_CACHE: ispn
  KC_CACHE_STACK: tcp
```

## Features

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_FEATURES` | Features adicionais | - | `preview` |
| `KC_FEATURES_DISABLED` | Features desabilitadas | - | `impersonation` |

```yaml
# Habilitar features preview
environment:
  KC_FEATURES: preview

# Desabilitar feature específica
environment:
  KC_FEATURES_DISABLED: impersonation
```

## Temas

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_SPI_THEME_STATIC_MAX_AGE` | Cache de assets (segundos) | `2592000` | `-1` |
| `KC_SPI_THEME_CACHE_THEMES` | Cache de temas | `true` | `false` |
| `KC_SPI_THEME_CACHE_TEMPLATES` | Cache de templates | `true` | `false` |
| `KC_SPI_THEME_DEFAULT` | Tema default por tipo | - | Ver abaixo |

```yaml
# Desenvolvimento (sem cache)
environment:
  KC_SPI_THEME_STATIC_MAX_AGE: -1
  KC_SPI_THEME_CACHE_THEMES: false
  KC_SPI_THEME_CACHE_TEMPLATES: false

# Produção
environment:
  KC_SPI_THEME_STATIC_MAX_AGE: 2592000
  KC_SPI_THEME_CACHE_THEMES: true
```

## Realm Import

| Variável | Descrição | Valor Padrão | Exemplo |
|:---------|:----------|:-------------|:--------|
| `KC_SPI_IMPORT_DIR` | Diretório de imports | - | `/import` |

**Command line:**
```bash
# Import no startup
/opt/keycloak/bin/kc.sh start --import-realm

# Import específico
/opt/keycloak/bin/kc.sh import --file /import/realm-carf.json
```

## Docker Compose Exemplo Completo

```yaml
# docker-compose.yml
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0.0
    command:
      - start
      - --import-realm
    environment:
      # Admin
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}

      # Database
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${KC_DB_PASSWORD}
      KC_DB_POOL_MIN_SIZE: 5
      KC_DB_POOL_MAX_SIZE: 20

      # Hostname
      KC_HOSTNAME: ${KC_HOSTNAME:-localhost}
      KC_HOSTNAME_STRICT: ${KC_HOSTNAME_STRICT:-false}
      KC_HOSTNAME_STRICT_HTTPS: ${KC_HOSTNAME_STRICT_HTTPS:-false}

      # HTTP/Proxy
      KC_HTTP_ENABLED: true
      KC_PROXY: ${KC_PROXY:-none}

      # Health/Metrics
      KC_HEALTH_ENABLED: true
      KC_METRICS_ENABLED: true

      # Logging
      KC_LOG_LEVEL: ${KC_LOG_LEVEL:-info}
      KC_LOG_CONSOLE_FORMAT: json

      # Cache
      KC_CACHE: local

      # Theme
      KC_SPI_THEME_CACHE_THEMES: ${KC_THEME_CACHE:-true}
    ports:
      - "8080:8080"
    volumes:
      - ./themes/carf:/opt/keycloak/themes/carf:ro
      - ./realm-export.json:/opt/keycloak/data/import/realm-carf.json:ro
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "exec 3<>/dev/tcp/127.0.0.1/8080"]
      interval: 10s
      timeout: 5s
      retries: 5

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: ${KC_DB_PASSWORD}
    volumes:
      - keycloak_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U keycloak"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  keycloak_db:
```

**.env exemplo:**
```bash
KC_ADMIN_PASSWORD=super-secret-admin-password
KC_DB_PASSWORD=super-secret-db-password
KC_HOSTNAME=keycloak.carf.gov.br
KC_HOSTNAME_STRICT=true
KC_HOSTNAME_STRICT_HTTPS=true
KC_PROXY=edge
KC_LOG_LEVEL=warn
KC_THEME_CACHE=true
```

## Referências

- [Keycloak Server Configuration](https://keycloak.org/server/configuration)
- [Keycloak All Configuration](https://keycloak.org/server/all-config)
- [Keycloak Containers](https://keycloak.org/server/containers)
