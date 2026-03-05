# CARF — Deploy

Infraestrutura de deploy do sistema CARF.
Atualmente suporta o ambiente **HML (Homologacao)**.

## Estrutura

```
PROJECTS/DEPLOY/
├── README.md                  ← voce esta aqui
├── dockerfiles/
│   ├── frontend.Dockerfile    # Build compartilhado (REURBWEB + REURBMASTER)
│   └── keycloak.Dockerfile    # Keycloak + tema CARF (build do carf-keycloak)
└── hml/
    ├── docker-compose.yml     # Stack completa HML (10 servicos)
    ├── .env.example           # Template de variaveis
    ├── deploy.sh              # Script de deploy por servico
    ├── repos.sh               # Clone/pull de todos os repos
    ├── POST-DEPLOY.md         # Verificacao pos-deploy (quase tudo e automatico)
    ├── nginx/
    │   └── default.conf.template  # Reverse proxy (sslip.io)
    └── scripts/
        ├── keycloak-init.sh   # Config automatica: SSL, URIs, user, roles, tema
        └── setup-vps.sh       # Setup inicial Ubuntu 24.04
```

## Arquitetura HML

```
                    ┌─────────────┐
  Internet ────────>│  nginx :80  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐───────────────┐
           ▼               ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  REURBWEB  │  │REURBMASTER │  │   GEOAPI   │  │  Keycloak  │
    │  (nginx)   │  │  (nginx)   │  │  (.NET 9)  │  │   (v26)    │
    └────────────┘  └────────────┘  └─────┬──────┘  └──────┬─────┘
                                          │                │
                    ┌─────────────────────┼────────────────┘
                    ▼           ▼         ▼
              ┌──────────┐ ┌───────┐ ┌────────┐ ┌───────┐
              │ PostGIS  │ │ Redis │ │ MinIO  │ │KC-DB  │
              │ (main)   │ │       │ │ (S3)   │ │(pg16) │
              └──────────┘ └───────┘ └────────┘ └───────┘
```

## URLs HML

| URL | Servico | Porta interna |
|-----|---------|---------------|
| `hml-app.{IP}.sslip.io` | REURBWEB | 80 |
| `hml-admin.{IP}.sslip.io` | REURBMASTER | 80 |
| `hml-api.{IP}.sslip.io` | GEOAPI + Swagger | 8080 |
| `hml-auth.{IP}.sslip.io` | Keycloak | 8080 |
| `hml-s3.{IP}.sslip.io` | MinIO Console | 9001 |
| `hml-storage.{IP}.sslip.io` | MinIO API | 9000 |

## Quick Start — Deploy inicial

### 1. Preparar o VPS (uma vez)

```bash
# No VPS como root
curl -fsSL https://raw.githubusercontent.com/carffundiaria/CARF/main/PROJECTS/DEPLOY/hml/scripts/setup-vps.sh | bash
# Ou: scp scripts/setup-vps.sh root@IP: && ssh root@IP bash setup-vps.sh
```

Cria: Docker, usuario `deploy`, firewall (22/80/443), swap 2GB.

### 2. Clonar repos

```bash
su - deploy
curl -fsSL https://raw.githubusercontent.com/carffundiaria/CARF/main/PROJECTS/DEPLOY/hml/repos.sh | bash
# Ou copiar repos.sh para o VPS e rodar: bash repos.sh
```

Resultado: `~/carf/` com todos os repos na estrutura correta.

### 3. Configurar .env

```bash
cd ~/carf/PROJECTS/DEPLOY/hml
cp .env.example .env
nano .env
# Preencher: VPS_IP, senhas, NPM_TOKEN, GOOGLE_MAPS_KEY
```

### 4. Subir stack

```bash
docker compose up -d --build
docker compose ps    # todos devem ficar healthy em ~2min
```

### 5. Verificar configuracao automatica

O container `keycloak-init` configura tudo automaticamente (SSL, redirect URIs, usuario seed, roles, tema CARF).

```bash
docker logs carf-hml-keycloak-init   # todos os [ok] = sucesso
```

Ver `POST-DEPLOY.md` para verificacao manual do geoapi-admin secret e troubleshooting.

## Operacoes comuns

### Atualizar um servico

```bash
bash deploy.sh geoapi       # pull + rebuild geoapi
bash deploy.sh reurbweb     # pull + rebuild reurbweb
bash deploy.sh reurbmaster  # pull + rebuild reurbmaster
bash deploy.sh frontends    # pull + rebuild ambos frontends
bash deploy.sh all          # pull tudo + rebuild tudo
```

### Ver logs

```bash
docker compose logs -f geoapi       # um servico
docker compose logs --tail 50       # ultimas 50 linhas de todos
```

### Rebuild sem cache (apos mudar Dockerfile)

```bash
docker compose build --no-cache reurbweb reurbmaster
docker compose up -d reurbweb reurbmaster
```

### Restart individual

```bash
docker compose restart keycloak
docker compose restart geoapi
```

### Limpar tudo e recomecar

```bash
docker compose down -v   # CUIDADO: apaga todos os volumes (dados)
docker compose up -d --build
```

## Gestao do NPM_TOKEN

Os frontends precisam de um token para baixar `@carffundiaria/*` do GitHub Packages.

| Tipo | Formato | Duracao | Como obter |
|------|---------|---------|------------|
| PAT classico | `ghp_*` | Permanente (ou custom) | github.com/settings/tokens/new → scope `read:packages` → "Configure SSO" → Authorize `carffundiaria` |
| gh CLI token | `gho_*` | Sessao do gh | `gh auth token` (precisa de `write:packages` no auth) |

**Recomendado**: PAT classico com scope minimo (`read:packages`), SSO authorized.

Para testar:
```bash
curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer SEU_TOKEN" \
  https://npm.pkg.github.com/@carffundiaria/ui
# 200 = OK
```

## Volumes persistentes

| Volume | Dados |
|--------|-------|
| `carf-hml-pgdata` | PostgreSQL principal (entidades, unidades, etc) |
| `carf-hml-kc-pgdata` | Keycloak DB (users, clients, sessions) |
| `carf-hml-redis` | Cache Redis |
| `carf-hml-minio` | Arquivos S3 (documentos, ortofotos) |

**Backup**: `docker run --rm -v carf-hml-pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata.tar.gz /data`

## Gotchas conhecidos

| Problema | Causa | Solucao |
|----------|-------|---------|
| GEOAPI 500 "RequireHttpsMetadata" | Keycloak roda HTTP, .NET exige HTTPS | `ASPNETCORE_ENVIRONMENT: Development` no compose |
| Keycloak admin 401 | Volume persistiu senha anterior | bootstrap-admin (ver POST-DEPLOY.md) |
| Frontend build 403 | Token sem acesso ao GitHub Packages | Trocar NPM_TOKEN (ver .env.example) |
| Frontend "unhealthy" | Alpine IPv6: `localhost` → `::1` | Dockerfile usa `127.0.0.1` |
| Keycloak "HTTPS required" (API externa) | KC_HOSTNAME forca HTTPS externamente | Usar kcadm.sh dentro do container |
| GEOAPI healthcheck 404 | Dockerfile usa `/health/live`, endpoint e `/health` | Compose override aponta para `/swagger/index.html` |
| Keycloak issuer tem `:8080` | KC_HOSTNAME nao inclui porta do proxy | Normal em HML, frontends lidam com isso |

## Ambiente atual (Mar 2026)

- **VPS**: 187.77.61.20 (KVM)
- **SSH**: `ssh -i ~/.ssh/carf_hml_deploy deploy@187.77.61.20`
- **Stack**: 9 containers Docker, todos healthy
- **Keycloak**: realm `carf`, Keycloak 26.0, start-dev mode
- **Usuario teste**: `admin.hml` / `Dev@1234` (super-admin + admin + dev, tenant `default`)
- **NPM_TOKEN**: `gho_*` do gh CLI (temporario — substituir por PAT classico)
