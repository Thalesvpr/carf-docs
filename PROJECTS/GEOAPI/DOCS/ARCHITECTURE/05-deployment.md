---
type: leaf
status: review
updated: 2026-02-08
---

# Deployment

Documentacao completa do processo de deployment da GEOAPI, cobrindo build Docker, registry, Kubernetes, escalabilidade e operacoes.

## Docker Build

### Dockerfile Multi-Stage

O Dockerfile utiliza build multi-stage para otimizar o tamanho da imagem final:

**Stage 1 — Build (SDK)**

| Aspecto | Valor |
|---------|-------|
| Imagem base | mcr.microsoft.com/dotnet/sdk:9.0-alpine |
| Workdir | /src |
| Operacoes | Restore de pacotes NuGet, build da solution, publish com otimizacoes |
| Artefatos | Binarios compilados em /app/publish |

**Stage 2 — Runtime (ASP.NET)**

| Aspecto | Valor |
|---------|-------|
| Imagem base | mcr.microsoft.com/dotnet/aspnet:9.0-alpine |
| Workdir | /app |
| Operacoes | Copia artefatos do stage build, configura ASPNETCORE_URLS, expoe porta 8080 |
| Tamanho final | ~200 MB |
| Healthcheck | HEALTHCHECK CMD curl -f http://localhost:8080/health/live || exit 1 |

### Build Args

| Arg | Descricao | Exemplo |
|-----|-----------|---------|
| DOTNET_VERSION | Versao do SDK .NET | 9.0 |
| CONFIGURATION | Configuracao de build | Release |
| PUBLISH_FLAGS | Flags extras de publish | --no-self-contained |

### Otimizacao de Tamanho

- Imagem Alpine (menor que Debian/Ubuntu)
- Multi-stage elimina SDK e ferramentas de build da imagem final
- Trim de assemblies nao utilizados via PublishTrimmed (avaliado, mas desabilitado por compatibilidade com reflection)
- Layer caching: COPY *.csproj antes de COPY . para cache de restore

## Container Registry

### Estrategia de Tagging

Cada build gera duas tags na imagem:

| Tag | Formato | Exemplo | Uso |
|-----|---------|---------|-----|
| Git SHA | git rev-parse --short HEAD | carf-geoapi:a1b2c3d | Rastreabilidade exata do commit |
| Semver | vMAJOR.MINOR.PATCH | carf-geoapi:v1.2.3 | Releases oficiais |
| Latest | latest | carf-geoapi:latest | Conveniencia para dev (nao usar em producao) |

### Push para Registry

```
docker build -t registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) .
docker tag registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) registry.example.com/carf-geoapi:latest
docker push registry.example.com/carf-geoapi:$(git rev-parse --short HEAD)
docker push registry.example.com/carf-geoapi:latest
```

## Kubernetes Manifests

### Deployment

| Propriedade | Staging | Producao |
|-------------|---------|----------|
| replicas | 2 | 3 |
| strategy.type | RollingUpdate | RollingUpdate |
| strategy.rollingUpdate.maxSurge | 1 | 1 |
| strategy.rollingUpdate.maxUnavailable | 0 | 0 |
| revisionHistoryLimit | 5 | 10 |
| terminationGracePeriodSeconds | 30 | 60 |

### Service

| Propriedade | Valor |
|-------------|-------|
| type | ClusterIP |
| port | 80 |
| targetPort | 8080 |
| protocol | TCP |

### Ingress

| Propriedade | Staging | Producao |
|-------------|---------|----------|
| ingressClassName | nginx | nginx |
| host | staging-api.carf.example.com | api.carf.example.com |
| TLS | Let's Encrypt (staging) | Let's Encrypt (production) |
| annotations | rate-limit: 100 req/s | rate-limit: 500 req/s |

### ConfigMap (Dados Nao-Sensiveis)

| Chave | Exemplo | Descricao |
|-------|---------|-----------|
| ASPNETCORE_ENVIRONMENT | Production | Ambiente de execucao |
| DATABASE_HOST | postgres-service | Host do PostgreSQL |
| DATABASE_PORT | 5432 | Porta do PostgreSQL |
| DATABASE_NAME | carf_db | Nome do banco |
| REDIS_HOST | redis-service | Host do Redis |
| REDIS_PORT | 6379 | Porta do Redis |
| KEYCLOAK_AUTHORITY | https://auth.carf.example.com/realms/carf | URL do Keycloak |
| S3_ENDPOINT | https://s3.sa-east-1.amazonaws.com | Endpoint S3 |
| S3_BUCKET | carf-documents | Nome do bucket |
| S3_REGION | sa-east-1 | Regiao AWS |
| HANGFIRE_WORKER_COUNT | 4 | Numero de workers Hangfire |
| CORS_ORIGINS | https://app.carf.example.com | Origens CORS permitidas |

### Secrets (Dados Sensiveis)

| Chave | Descricao | Gerenciamento |
|-------|-----------|--------------|
| DATABASE_PASSWORD | Senha do PostgreSQL | Kubernetes Secret (sealed) |
| REDIS_PASSWORD | Senha do Redis | Kubernetes Secret (sealed) |
| KEYCLOAK_CLIENT_SECRET | Client secret do Keycloak | Kubernetes Secret (sealed) |
| S3_ACCESS_KEY | AWS Access Key | Kubernetes Secret (sealed) |
| S3_SECRET_KEY | AWS Secret Key | Kubernetes Secret (sealed) |
| JWT_SECRET | Chave de validacao JWT | Kubernetes Secret (sealed) |

## Resource Limits

| Ambiente | CPU Request | CPU Limit | Memory Request | Memory Limit |
|----------|-----------|-----------|---------------|-------------|
| Development | 100m | 500m | 256Mi | 512Mi |
| Staging | 250m | 500m | 512Mi | 1Gi |
| Production | 250m | 1000m | 512Mi | 2Gi |

### Justificativa

- **CPU Request 250m**: garante scheduling adequado, API e I/O-bound (banco, S3, Redis)
- **Memory Request 512Mi**: .NET runtime + EF Core + connection pools
- **Memory Limit 2Gi (prod)**: margem para picos de processamento (relatorios, ortofotos)
- **Sem CPU Limit em dev**: permite burst para melhor experiencia de desenvolvimento

## Horizontal Pod Autoscaler (HPA)

| Propriedade | Staging | Producao |
|-------------|---------|----------|
| minReplicas | 2 | 3 |
| maxReplicas | 5 | 10 |
| CPU targetUtilization | 70% | 70% |
| Memory targetUtilization | 80% | 80% |
| scaleDown.stabilizationWindowSeconds | 60 | 300 |
| scaleUp.stabilizationWindowSeconds | 30 | 60 |

### Metricas Customizadas (Futuro)

Alem de CPU e memoria, o HPA pode escalar com base em:
- Requests por segundo (via Prometheus adapter)
- Profundidade da fila Hangfire
- Numero de conexoes SignalR ativas

## Health Checks

### Endpoints

| Endpoint | Tipo | Descricao | Checks Incluidos |
|----------|------|-----------|-----------------|
| /health/live | Liveness | Aplicacao esta viva e respondendo | Verifica se o processo responde HTTP |
| /health/ready | Readiness | Aplicacao esta pronta para receber trafego | PostgreSQL, Redis, Keycloak, S3 |
| /health/startup | Startup | Aplicacao terminou de inicializar | Migrations aplicadas, cache aquecido |

### Configuracao de Probes no Kubernetes

| Probe | Endpoint | initialDelaySeconds | periodSeconds | timeoutSeconds | failureThreshold |
|-------|----------|-------------------|--------------|---------------|-----------------|
| livenessProbe | /health/live | 10 | 30 | 5 | 3 |
| readinessProbe | /health/ready | 15 | 10 | 5 | 3 |
| startupProbe | /health/startup | 5 | 5 | 5 | 12 |

### Comportamento de Falha

- **Liveness falha**: Kubernetes reinicia o pod (kill + recreate)
- **Readiness falha**: Kubernetes remove o pod do Service (para de enviar trafego)
- **Startup falha**: Kubernetes nao envia liveness/readiness ate startup passar (maximo 60s = 12 x 5s)

### Detalhes do Readiness Check

| Dependencia | Timeout | Metodo |
|-------------|---------|--------|
| PostgreSQL | 3s | Executa SELECT 1 |
| Redis | 2s | Executa PING |
| Keycloak | 5s | HTTP GET no well-known endpoint |
| S3 | 3s | HEAD no bucket |

## Secrets Management

### Hierarquia de Configuracao

Ordem de precedencia (ultimo vence):

1. `appsettings.json` — valores default
2. `appsettings.{Environment}.json` — valores por ambiente
3. Variaveis de ambiente — ConfigMap do Kubernetes
4. Kubernetes Secrets — montados como variaveis de ambiente ou volumes

### Sealed Secrets

Em producao, Secrets Kubernetes sao criptografados com Sealed Secrets (Bitnami):

1. Desenvolvedor cria SealedSecret com kubeseal
2. SealedSecret e versionado no Git (seguro — criptografado)
3. Controller no cluster decripta e cria o Secret real
4. Pod monta o Secret como variavel de ambiente

### Rotacao de Secrets

| Secret | Rotacao | Procedimento |
|--------|---------|-------------|
| DATABASE_PASSWORD | Trimestral | Alterar no PostgreSQL + atualizar Secret + rolling restart |
| KEYCLOAK_CLIENT_SECRET | Trimestral | Regenerar no Keycloak + atualizar Secret + rolling restart |
| S3_ACCESS_KEY / S3_SECRET_KEY | Semestral | Criar nova key no IAM + atualizar Secret + remover key antiga |

## Rolling Update Strategy

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| maxSurge | 1 | Cria no maximo 1 pod extra durante update |
| maxUnavailable | 0 | Nenhum pod indisponivel durante update (zero downtime) |

### Sequencia de Rolling Update

1. Kubernetes cria 1 pod novo com a nova imagem
2. Novo pod executa startupProbe ate passar
3. Novo pod comeca a receber trafego (readinessProbe OK)
4. Kubernetes termina 1 pod antigo (envia SIGTERM, graceful shutdown)
5. Pod antigo drena conexoes em andamento (terminationGracePeriodSeconds)
6. Repete ate todos os pods serem atualizados

### Rollback Automatico

Se o novo pod falhar no readinessProbe 3 vezes consecutivas:

1. Kubernetes nao envia trafego para o pod novo
2. O pod antigo continua recebendo trafego normalmente
3. Apos progressDeadlineSeconds (600s), o rollout e marcado como falhado
4. Rollback manual: `kubectl rollout undo deployment/geoapi -n production`

## Database Migration Job

Migrations sao executadas via Kubernetes Job antes do deployment da aplicacao.

### Fluxo

1. CI/CD cria o Job de migration com a mesma imagem do deployment
2. Job executa: `dotnet ef database update` (aplica migrations pendentes)
3. Job aguarda PostgreSQL estar healthy via init container
4. Se o Job falhar, o deployment nao prossegue (pipeline falha)
5. Se o Job suceder, deployment prossegue com rolling update

### Configuracao do Job

| Propriedade | Valor |
|-------------|-------|
| backoffLimit | 3 |
| activeDeadlineSeconds | 300 |
| ttlSecondsAfterFinished | 3600 |
| restartPolicy | Never |

### Rollback de Migration

Em caso de necessidade de rollback de migration:

1. Identificar a migration anterior: `dotnet ef migrations list`
2. Executar rollback: `dotnet ef database update PreviousMigrationName`
3. Remover migration do codigo: `dotnet ef migrations remove`

Atencao: rollback de migrations que removem colunas ou tabelas pode causar perda de dados. Sempre verificar o script SQL gerado antes de aplicar.

## Ambientes

### Development (Local)

| Componente | Ferramenta |
|-----------|------------|
| Orquestracao | Docker Compose |
| PostgreSQL | Container local (porta 5432) |
| Redis | Container local (porta 6379) |
| Keycloak | Container local (porta 8080) |
| MinIO | Container local (porta 9000/9001) |
| GEOAPI | dotnet run com hot reload |

### Staging

| Componente | Ferramenta |
|-----------|------------|
| Orquestracao | Kubernetes (namespace staging) |
| PostgreSQL | Instancia dedicada (dados anonimizados) |
| Redis | Instancia dedicada |
| Keycloak | Instancia compartilhada (realm staging) |
| S3 | Bucket dedicado (carf-staging-documents) |
| GEOAPI | 2 replicas |

### Production

| Componente | Ferramenta |
|-----------|------------|
| Orquestracao | Kubernetes (namespace production) |
| PostgreSQL | RDS Multi-AZ (backups automaticos) |
| Redis | ElastiCache Cluster (3 masters + 3 replicas) |
| Keycloak | Instancia dedicada (HA com 2 replicas) |
| S3 | Bucket dedicado (carf-documents, versionado) |
| GEOAPI | 3-10 replicas (HPA) |

## CI/CD Pipeline

### Trigger

- Push na branch `main` → deploy automatico em staging
- Tag `v*` → deploy automatico em producao (com aprovacao manual)
- Pull Request → build + test (sem deploy)

### Steps

| Step | Descricao | Timeout |
|------|-----------|---------|
| Restore | dotnet restore | 2min |
| Build | dotnet build -c Release | 3min |
| Test | dotnet test (unit + integration) | 5min |
| Publish | dotnet publish -c Release -o out | 2min |
| Docker Build | docker build -t carf-geoapi:TAG . | 3min |
| Docker Push | docker push registry/carf-geoapi:TAG | 2min |
| Migration Job | kubectl apply migration job | 5min |
| Deploy | kubectl set image deployment/geoapi | 5min |
| Verify | kubectl rollout status deployment/geoapi | 5min |
| Smoke Test | curl health endpoint + API test | 2min |