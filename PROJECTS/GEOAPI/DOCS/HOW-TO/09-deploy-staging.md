---
type: leaf
status: review
updated: 2026-02-08
---

# Deploy para Staging

Guia passo-a-passo para realizar deploy manual da GEOAPI no ambiente de staging. Este procedimento e normalmente automatizado via CI/CD, mas pode ser executado manualmente em caso de necessidade.

## Pre-Requisitos

| Ferramenta | Versao Minima | Verificar |
|-----------|--------------|-----------|
| .NET SDK | 9.0 | `dotnet --version` |
| Docker | 24.0+ | `docker --version` |
| kubectl | 1.28+ | `kubectl version --client` |
| Acesso ao registry | - | `docker login registry.example.com` |
| Kubeconfig staging | - | `kubectl config use-context staging` |

## Passo 1: Build da Aplicacao

Compilar e publicar a aplicacao em modo Release:

```
dotnet restore src/Carf.GeoApi.sln
dotnet build src/Carf.GeoApi.sln -c Release --no-restore
dotnet publish src/Carf.GeoApi.Gateway/Carf.GeoApi.Gateway.csproj -c Release -o out --no-build
```

Verificar que o diretorio `out/` contem os binarios compilados e o `Carf.GeoApi.Gateway.dll`.

## Passo 2: Executar Testes

Executar a suite de testes antes de prosseguir com o deploy:

```
dotnet test src/Carf.GeoApi.sln -c Release --no-build --verbosity normal
```

Todos os testes devem passar. Nao fazer deploy se houver falhas.

## Passo 3: Build da Imagem Docker

Construir a imagem Docker com tag baseada no SHA do commit:

```
docker build -t registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) .
```

Opcionalmente, adicionar tag semver se for um release:

```
docker tag registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) registry.example.com/carf-geoapi:v1.2.3
```

## Passo 4: Push da Imagem

Enviar a imagem para o container registry:

```
docker push registry.example.com/carf-geoapi:$(git rev-parse --short HEAD)
```

Verificar que a imagem aparece no registry:

```
docker manifest inspect registry.example.com/carf-geoapi:$(git rev-parse --short HEAD)
```

## Passo 5: Executar Migrations

Executar as migrations do banco de dados no ambiente staging antes de atualizar a aplicacao:

```
kubectl run migration-$(date +%Y%m%d%H%M%S) \
  --namespace=staging \
  --image=registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) \
  --restart=Never \
  --env="DATABASE_CONNECTION_STRING=$(kubectl get secret geoapi-secrets -n staging -o jsonpath='{.data.DATABASE_CONNECTION_STRING}' | base64 -d)" \
  -- dotnet ef database update --project src/Carf.GeoApi.Infrastructure/Carf.GeoApi.Infrastructure.csproj --startup-project src/Carf.GeoApi.Gateway/Carf.GeoApi.Gateway.csproj
```

Aguardar conclusao do Job:

```
kubectl wait --for=condition=complete job/migration-TIMESTAMP -n staging --timeout=300s
```

Verificar logs do Job para confirmar sucesso:

```
kubectl logs job/migration-TIMESTAMP -n staging
```

## Passo 6: Aplicar Manifests Kubernetes

Atualizar a imagem no deployment de staging:

```
kubectl set image deployment/geoapi geoapi=registry.example.com/carf-geoapi:$(git rev-parse --short HEAD) -n staging
```

Ou, se houver alteracoes nos manifests (ConfigMap, resources, etc.):

```
kubectl apply -f k8s/staging/
```

## Passo 7: Verificar Rollout

Acompanhar o status do rolling update:

```
kubectl rollout status deployment/geoapi -n staging --timeout=300s
```

Saida esperada: `deployment "geoapi" successfully rolled out`

Verificar que todos os pods estao Running e Ready:

```
kubectl get pods -n staging -l app=geoapi
```

Saida esperada: todos os pods com STATUS `Running` e READY `1/1`.

## Passo 8: Health Check

Verificar que a aplicacao esta saudavel:

```
curl -s https://staging-api.carf.example.com/health | jq .
```

Resposta esperada:

```
{
  "status": "Healthy",
  "checks": {
    "postgresql": "Healthy",
    "redis": "Healthy",
    "keycloak": "Healthy",
    "s3": "Healthy"
  }
}
```

Verificar readiness:

```
curl -s https://staging-api.carf.example.com/health/ready
```

Verificar liveness:

```
curl -s https://staging-api.carf.example.com/health/live
```

## Passo 9: Smoke Test

Executar um teste basico de criacao via API para confirmar funcionamento:

### 9.1 Obter Token de Acesso

```
TOKEN=$(curl -s -X POST \
  https://staging-auth.carf.example.com/realms/carf/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=geoapi-staging" \
  -d "client_secret=STAGING_SECRET" \
  | jq -r '.access_token')
```

### 9.2 Criar Unidade de Teste

```
curl -s -X POST https://staging-api.carf.example.com/api/units \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: staging-tenant-id" \
  -d '{
    "communityId": "staging-community-id",
    "address": {
      "street": "Rua de Teste",
      "number": "123"
    }
  }' | jq .
```

Resposta esperada: HTTP 201 Created com o UnitDto no body.

### 9.3 Verificar Unidade Criada

```
UNIT_ID=$(curl -s -X GET "https://staging-api.carf.example.com/api/units?pageSize=1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: staging-tenant-id" \
  | jq -r '.items[0].id')

curl -s https://staging-api.carf.example.com/api/units/$UNIT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: staging-tenant-id" | jq .
```

## Rollback

Se algo der errado apos o deploy, executar rollback imediato:

```
kubectl rollout undo deployment/geoapi -n staging
```

Verificar que o rollback foi bem-sucedido:

```
kubectl rollout status deployment/geoapi -n staging
```

### Rollback de Migration

Se a migration causou problemas, identificar e reverter:

```
# Listar migrations aplicadas
kubectl exec -it deployment/geoapi -n staging -- dotnet ef migrations list

# Reverter para migration anterior
kubectl run rollback-$(date +%Y%m%d%H%M%S) \
  --namespace=staging \
  --image=registry.example.com/carf-geoapi:PREVIOUS_TAG \
  --restart=Never \
  -- dotnet ef database update NomeMigrationAnterior
```

## Checklist de Deploy

| Etapa | Comando de Verificacao | Resultado Esperado |
|-------|----------------------|-------------------|
| Testes passaram | `dotnet test` | 0 falhas |
| Imagem buildou | `docker images \| grep carf-geoapi` | Imagem com tag correta |
| Imagem no registry | `docker manifest inspect` | Manifest encontrado |
| Migration executou | `kubectl logs job/migration-*` | "Done." no log |
| Rollout completo | `kubectl rollout status` | "successfully rolled out" |
| Health OK | `curl /health` | {"status": "Healthy"} |
| Smoke test OK | `curl POST /api/units` | HTTP 201 |

## Troubleshooting

| Problema | Diagnostico | Solucao |
|----------|------------|---------|
| Pod em CrashLoopBackOff | `kubectl logs pod/NAME -n staging` | Verificar variaveis de ambiente e conexoes |
| Migration falhou | `kubectl logs job/migration-* -n staging` | Verificar SQL gerado, corrigir e reexecutar |
| Readiness falha | `kubectl describe pod/NAME -n staging` | Verificar dependencias (PostgreSQL, Redis, Keycloak) |
| 502 Bad Gateway | `kubectl logs -l app=ingress-nginx -n ingress-nginx` | Verificar Service e Ingress config |
| Timeout na API | `kubectl top pods -n staging` | Verificar resource limits, escalar se necessario |