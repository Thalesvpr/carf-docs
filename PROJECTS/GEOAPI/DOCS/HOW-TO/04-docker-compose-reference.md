---
type: leaf
status: review
updated: 2026-02-08
---

# Docker Compose Reference - GEOAPI

Referencia completa do `docker-compose.yml` utilizado para desenvolvimento local do GEOAPI, incluindo todos os servicos de infraestrutura, variaveis de ambiente, volumes e rede.

---

## Visao Geral dos Servicos

| Servico | Imagem | Portas | Proposito |
|---------|--------|--------|-----------|
| postgres | `postgis/postgis:16-3.4` | `5432:5432` | Banco de dados relacional com extensao geoespacial PostGIS |
| redis | `redis:7-alpine` | `6379:6379` | Cache distribuido e session store |
| minio | `minio/minio:latest` | `9000:9000` (API), `9001:9001` (Console) | Object storage compativel com S3 para documentos e fotos |
| keycloak | `quay.io/keycloak/keycloak:23.0` | `8080:8080` | Identity provider (OAuth2/OIDC) para autenticacao e autorizacao |

---

## Servico: PostgreSQL + PostGIS

### Configuracao

| Propriedade | Valor |
|------------|-------|
| Container name | `geoapi-db` |
| Image | `postgis/postgis:16-3.4` |
| Ports | `5432:5432` |
| Restart policy | `unless-stopped` |

### Variaveis de Ambiente

| Variavel | Valor Padrao | Descricao |
|----------|-------------|-----------|
| `POSTGRES_DB` | `geoapi_dev` | Nome do banco de dados inicial |
| `POSTGRES_USER` | `geoapi` | Usuario principal do banco |
| `POSTGRES_PASSWORD` | `dev123` | Senha do usuario (apenas dev local) |
| `POSTGRES_INITDB_ARGS` | `--encoding=UTF-8 --lc-collate=pt_BR.UTF-8` | Encoding e collation para portugues |

### Volume

| Volume | Mount Path | Descricao |
|--------|-----------|-----------|
| `postgres_data` | `/var/lib/postgresql/data` | Persistencia dos dados do banco entre restarts |

### Healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U geoapi -d geoapi_dev"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 30s
```

### Verificacao Manual

```bash
# Verificar conectividade
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "SELECT 1;"

# Verificar extensao PostGIS
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "SELECT PostGIS_Version();"

# Listar tabelas
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "\dt"

# Verificar tamanho do banco
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "SELECT pg_size_pretty(pg_database_size('geoapi_dev'));"
```

---

## Servico: Redis

### Configuracao

| Propriedade | Valor |
|------------|-------|
| Container name | `geoapi-redis` |
| Image | `redis:7-alpine` |
| Ports | `6379:6379` |
| Restart policy | `unless-stopped` |

### Variaveis de Ambiente

Redis Alpine nao utiliza variaveis de ambiente. Configuracao via command line args.

### Command

```yaml
command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
```

| Flag | Descricao |
|------|-----------|
| `--appendonly yes` | Habilita persistencia AOF (Append Only File) |
| `--maxmemory 256mb` | Limite de memoria (ajustar conforme necessidade dev) |
| `--maxmemory-policy allkeys-lru` | Politica de eviction: remove chaves menos usadas recentemente |

### Volume

| Volume | Mount Path | Descricao |
|--------|-----------|-----------|
| `redis_data` | `/data` | Persistencia do arquivo AOF entre restarts |

### Healthcheck

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 3s
  retries: 5
```

### Verificacao Manual

```bash
# Testar conexao
docker exec -it geoapi-redis redis-cli ping
# Esperado: PONG

# Verificar info geral
docker exec -it geoapi-redis redis-cli info server | head -20

# Listar chaves (dev only)
docker exec -it geoapi-redis redis-cli keys "*"

# Verificar uso de memoria
docker exec -it geoapi-redis redis-cli info memory | grep used_memory_human
```

---

## Servico: MinIO (S3-Compatible)

### Configuracao

| Propriedade | Valor |
|------------|-------|
| Container name | `geoapi-minio` |
| Image | `minio/minio:latest` |
| Ports | `9000:9000` (API S3), `9001:9001` (Console Web) |
| Restart policy | `unless-stopped` |

### Variaveis de Ambiente

| Variavel | Valor Padrao | Descricao |
|----------|-------------|-----------|
| `MINIO_ROOT_USER` | `minioadmin` | Usuario root (equivalente a AWS Access Key) |
| `MINIO_ROOT_PASSWORD` | `minioadmin` | Senha root (equivalente a AWS Secret Key) |

### Command

```yaml
command: server /data --console-address ":9001"
```

### Volume

| Volume | Mount Path | Descricao |
|--------|-----------|-----------|
| `minio_data` | `/data` | Persistencia dos objetos (documentos, fotos) entre restarts |

### Healthcheck

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Configuracao Pos-Startup (Criar Buckets)

Apos o MinIO subir pela primeira vez, criar os buckets necessarios:

**Via Console Web:**

1. Acessar `http://localhost:9001` (login: minioadmin/minioadmin)
2. Menu lateral → Buckets → Create Bucket
3. Criar: `carf-documents`, `carf-orthofotos`, `carf-exports`

**Via MinIO Client (mc):**

```bash
# Instalar mc (se nao tiver)
# Windows: winget install minio.mc
# macOS: brew install minio/stable/mc
# Linux: curl -O https://dl.min.io/client/mc/release/linux-amd64/mc && chmod +x mc

# Configurar alias local
mc alias set local http://localhost:9000 minioadmin minioadmin

# Criar buckets
mc mb local/carf-documents
mc mb local/carf-orthofotos
mc mb local/carf-exports

# Verificar
mc ls local/
# Esperado: carf-documents/ carf-orthofotos/ carf-exports/
```

### Verificacao Manual

```bash
# Testar API S3
curl -f http://localhost:9000/minio/health/live
# Esperado: HTTP 200

# Listar buckets via mc
mc ls local/

# Verificar uso de disco
mc admin info local/
```

---

## Servico: Keycloak

### Configuracao

| Propriedade | Valor |
|------------|-------|
| Container name | `geoapi-keycloak` |
| Image | `quay.io/keycloak/keycloak:23.0` |
| Ports | `8080:8080` |
| Restart policy | `unless-stopped` |

### Variaveis de Ambiente

| Variavel | Valor Padrao | Descricao |
|----------|-------------|-----------|
| `KEYCLOAK_ADMIN` | `admin` | Usuario administrador do Keycloak |
| `KEYCLOAK_ADMIN_PASSWORD` | `admin` | Senha do administrador (apenas dev) |
| `KC_HEALTH_ENABLED` | `true` | Habilitar endpoint de health check |
| `KC_METRICS_ENABLED` | `true` | Habilitar metricas Prometheus |

### Command

```yaml
command: start-dev
```

> `start-dev` inicia Keycloak em modo desenvolvimento (sem HTTPS, banco H2 embarcado, hot-deploy de temas). Para producao usar `start` com banco PostgreSQL externo.

### Healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "exec 3<>/dev/tcp/localhost/8080 && echo -e 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3 && cat <&3 | grep -q '\"status\": \"UP\"'"]
  interval: 15s
  timeout: 10s
  retries: 10
  start_period: 60s
```

> **Nota:** Keycloak demora mais para inicializar (30-60s). O `start_period` de 60s evita falsos alertas de healthcheck.

### Verificacao Manual

```bash
# Health check
curl -s http://localhost:8080/health/ready | jq .
# Esperado: { "status": "UP", "checks": [...] }

# Verificar realm CARF existe
curl -s http://localhost:8080/realms/carf/.well-known/openid-configuration | jq .issuer
# Esperado: "http://localhost:8080/realms/carf"
```

---

## Rede

Todos os servicos operam na mesma bridge network:

```yaml
networks:
  carf-network:
    driver: bridge
    name: carf-network
```

### Resolucao de Nomes Interna

Dentro da rede `carf-network`, cada servico e acessivel pelo nome do container:

| De (container) | Para (container) | Endereco Interno |
|----------------|-----------------|-----------------|
| API (.NET) | PostgreSQL | `geoapi-db:5432` |
| API (.NET) | Redis | `geoapi-redis:6379` |
| API (.NET) | MinIO | `geoapi-minio:9000` |
| API (.NET) | Keycloak | `geoapi-keycloak:8080` |

> Quando a API roda fora do Docker (na maquina host), usar `localhost` nas connection strings.

---

## Volumes

| Volume | Servico | Descricao | Dados Persistidos |
|--------|---------|-----------|-------------------|
| `postgres_data` | postgres | Dados do PostgreSQL | Tabelas, indices, migrations aplicadas |
| `redis_data` | redis | Arquivo AOF do Redis | Chaves de cache persistidas |
| `minio_data` | minio | Objetos armazenados | Documentos, fotos, ortofotos |

### Listar Volumes

```bash
docker volume ls | grep carf
# Esperado:
# local   carf-geoapi_postgres_data
# local   carf-geoapi_redis_data
# local   carf-geoapi_minio_data
```

---

## Comandos Frequentes

### Ciclo de Vida

| Comando | Descricao |
|---------|-----------|
| `docker compose up -d` | Iniciar todos os servicos em background |
| `docker compose down` | Parar e remover containers (volumes preservados) |
| `docker compose down -v` | Parar, remover containers E volumes (reset completo) |
| `docker compose restart` | Reiniciar todos os servicos |
| `docker compose restart postgres` | Reiniciar apenas PostgreSQL |

### Monitoramento

| Comando | Descricao |
|---------|-----------|
| `docker compose ps` | Ver status de todos os servicos |
| `docker compose logs -f` | Acompanhar logs de todos os servicos em tempo real |
| `docker compose logs -f postgres` | Logs apenas do PostgreSQL |
| `docker compose logs --tail=50 keycloak` | Ultimas 50 linhas do Keycloak |
| `docker stats` | Uso de CPU/memoria de todos os containers |

### Manutencao

| Comando | Descricao |
|---------|-----------|
| `docker compose pull` | Atualizar imagens para latest |
| `docker compose build --no-cache` | Rebuild sem cache (se houver custom Dockerfile) |
| `docker system prune -a` | Limpar imagens/containers/volumes nao utilizados |
| `docker volume prune` | Remover volumes orfaos |

---

## Reset Completo do Ambiente

Quando necessario comecar do zero:

```bash
# 1. Parar e remover tudo (containers + volumes)
docker compose down -v

# 2. Subir servicos novamente
docker compose up -d

# 3. Aguardar healthchecks
sleep 60

# 4. Re-criar buckets MinIO
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/carf-documents
mc mb local/carf-orthofotos
mc mb local/carf-exports

# 5. Re-aplicar migrations
cd PROJECTS/GEOAPI/SRC-CODE
dotnet ef database update \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway

# 6. Re-importar realm Keycloak
docker cp PROJECTS/KEYCLOAK/DOCS/CONFIG/realm-export.json geoapi-keycloak:/tmp/
docker exec geoapi-keycloak /opt/keycloak/bin/kc.sh import \
  --file /tmp/realm-export.json --override true
```

---

## Troubleshooting Docker

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Container nao inicia | Porta ja em uso | `lsof -i :5432` (Linux/Mac) ou `netstat -ano \| findstr 5432` (Windows) para encontrar processo |
| `docker compose up` falha com "network not found" | Rede removida sem remover containers | `docker compose down` e depois `docker compose up -d` |
| Volume corrompido | Shutdown abrupto | `docker compose down -v` e re-criar |
| Container reiniciando em loop | Erro de configuracao | `docker compose logs <servico>` para diagnostico |
| Disco cheio | Volumes/imagens acumulados | `docker system prune -a --volumes` (cuidado: remove tudo) |
| Lentidao no macOS | Bind mounts lentos no macOS | Usar volumes nomeados ao inves de bind mounts para dados |
