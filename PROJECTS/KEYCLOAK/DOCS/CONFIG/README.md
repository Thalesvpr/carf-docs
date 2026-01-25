---
type: readme
status: review
description: "Usa tabelas e code blocks ao inves de prosa densa - reescrever em paragrafos"
updated: 2026-01-22
---

# CONFIG

Arquivos de configuracao para deploy e desenvolvimento do Keycloak no ambiente CARF.

## Arquivos

| Arquivo | Descricao |
|:--------|:----------|
| [docker-compose.yml](./docker-compose.yml) | Compose para ambiente de desenvolvimento local |
| [realm-export.json](./realm-export.json) | Export completo do realm CARF para import |
| [.env.example](./.env.example) | Template de variaveis de ambiente |

## Uso

### Desenvolvimento Local

```bash
# Copiar e configurar variaveis de ambiente
cp .env.example .env

# Subir Keycloak
docker-compose up -d

# Acessar Admin Console
open http://localhost:8080/admin
```

### Import do Realm

O arquivo `realm-export.json` contem a configuracao completa do realm CARF incluindo:

- Clients (geoweb, reurbcad, geoapi, geogis, webdocs, admin)
- Roles (user, field-agent, analyst, admin, super-admin, dev)
- Protocol Mappers (tenant_id, allowed_tenants)
- Authentication Flows
- Password Policy
- Brute Force Protection

Para importar em novo ambiente:

```bash
# Via CLI
/opt/keycloak/bin/kc.sh import --file=/path/to/realm-export.json

# Ou via Docker
docker run --rm \
  -v $(pwd)/realm-export.json:/tmp/realm.json \
  quay.io/keycloak/keycloak:latest \
  import --file=/tmp/realm.json
```

### Variaveis de Ambiente

Ver `.env.example` para lista completa. Principais:

| Variavel | Descricao | Exemplo |
|:---------|:----------|:--------|
| `KC_DB` | Tipo de banco | `postgres` |
| `KC_DB_URL` | Connection string | `jdbc:postgresql://db:5432/keycloak` |
| `KC_HOSTNAME` | Hostname publico | `auth.carf.example.com` |
| `KEYCLOAK_ADMIN` | Usuario admin | `admin` |
| `KEYCLOAK_ADMIN_PASSWORD` | Senha admin | (vault) |

## Ambientes

| Ambiente | Compose | Notas |
|:---------|:--------|:------|
| Local | `docker-compose.yml` | Cache de temas desabilitado |
| Staging | Kubernetes | Secrets via External Secrets |
| Production | Kubernetes | HA com 3 replicas |

## Ver Tambem

- [HOW-TO/03-setup-dev-environment](../HOW-TO/03-setup-dev-environment.md) - Setup completo de dev
- [HOW-TO/06-configure-production](../HOW-TO/06-configure-production.md) - Configuracao de producao
- [REFERENCE/05-environment-variables](../REFERENCE/05-environment-variables.md) - Todas variaveis

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

<!-- CARF-INDEX-END -->
