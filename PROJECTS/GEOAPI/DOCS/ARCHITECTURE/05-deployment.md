# Arquitetura de Deployment - GEOAPI

Este documento detalha a arquitetura de deployment do GEOAPI, incluindo containerização, orquestração, CI/CD e estratégias multi-ambiente.

## 📋 Índice

- [1. Visão Geral](#1-visão-geral)
- [2. Containerização com Docker](#2-containerização-com-docker)
- [3. Orquestração com Kubernetes](#3-orquestração-com-kubernetes)
- [4. CI/CD Pipeline](#4-cicd-pipeline)
- [5. Estratégia Multi-Ambiente](#5-estratégia-multi-ambiente)
- [6. Configuração e Secrets](#6-configuração-e-secrets)
- [7. Monitoramento e Observabilidade](#7-monitoramento-e-observabilidade)
- [8. Backup e Disaster Recovery](#8-backup-e-disaster-recovery)
- [9. Segurança no Deployment](#9-segurança-no-deployment)

---

## 1. Visão Geral

### 1.1 Arquitetura de Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRODUCTION ENVIRONMENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │               Kubernetes Cluster (AKS/GKE)                   ││
│  │                                                               ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       ││
│  │  │   Ingress    │  │   Ingress    │  │   Ingress    │       ││
│  │  │  Controller  │  │  Controller  │  │  Controller  │       ││
│  │  │  (nginx)     │  │  (nginx)     │  │  (nginx)     │       ││
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       ││
│  │         │                 │                 │                ││
│  │  ┌──────▼──────────────────▼─────────────────▼─────────┐    ││
│  │  │              Load Balancer Service                   │    ││
│  │  └──────┬────────────────────────────────────────┬──────┘    ││
│  │         │                                        │            ││
│  │  ┌──────▼─────────┐  ┌──────────────┐  ┌────────▼─────────┐ ││
│  │  │  GEOAPI Pod 1  │  │  GEOAPI  ...  │  │  GEOAPI Pod N   │ ││
│  │  │ (3 replicas)   │  │               │  │                  │ ││
│  │  │                │  │               │  │                  │ ││
│  │  │ Container:     │  │               │  │                  │ ││
│  │  │ - geoapi:v1.2  │  │               │  │                  │ ││
│  │  │ - Port: 8080   │  │               │  │                  │ ││
│  │  └────────────────┘  └───────────────┘  └──────────────────┘ ││
│  │                                                               ││
│  │  ┌──────────────────────────────────────────────────────┐    ││
│  │  │              Database (PostgreSQL)                   │    ││
│  │  │  - StatefulSet (Primary + 2 Replicas)               │    ││
│  │  │  - Persistent Volume (Azure Disk / GCP PD)          │    ││
│  │  │  - Automated Backups (hourly)                       │    ││
│  │  └──────────────────────────────────────────────────────┘    ││
│  │                                                               ││
│  │  ┌──────────────────────────────────────────────────────┐    ││
│  │  │              External Services                        │    ││
│  │  │  - Keycloak (auth.carf.gov.br)                       │    ││
│  │  │  - Elasticsearch (logs)                              │    ││
│  │  │  - Prometheus (metrics)                              │    ││
│  │  │  - Grafana (dashboards)                              │    ││
│  │  └──────────────────────────────────────────────────────┘    ││
│  └───────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         CI/CD PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│  GitHub → Build → Test → Docker Image → Push to Registry →      │
│  → Deploy to Staging → Integration Tests → Deploy to Prod       │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Componentes da Infraestrutura

| Componente | Tecnologia | Função |
|-----------|-----------|--------|
| **Container Runtime** | Docker | Empacotamento da aplicação |
| **Orchestração** | Kubernetes (AKS/GKE/EKS) | Gerenciamento de containers |
| **Ingress** | NGINX Ingress Controller | Roteamento HTTP/HTTPS |
| **Load Balancer** | Cloud Provider LB | Distribuição de tráfego |
| **Database** | PostgreSQL + PostGIS (StatefulSet) | Persistência de dados |
| **Storage** | Azure Disk / GCP Persistent Disk | Volumes persistentes |
| **Registry** | Azure Container Registry / GCR | Armazenamento de imagens Docker |
| **CI/CD** | GitHub Actions | Automação de build e deploy |
| **Monitoring** | Prometheus + Grafana | Métricas e dashboards |
| **Logging** | Elasticsearch + Kibana | Logs centralizados |
| **Secrets** | Kubernetes Secrets / Azure Key Vault | Gerenciamento de secrets |
| **DNS** | Azure DNS / Cloud DNS | Resolução de nomes |
| **CDN** | Azure CDN / Cloud CDN | Cache de assets estáticos |

---

## 2. Containerização com Docker

### 2.1 Dockerfile Multi-Stage

```dockerfile
# GEOAPI/Dockerfile

# ============================================
# Stage 1: Build
# ============================================
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy csproj files and restore dependencies
COPY ["src/GEOAPI.Gateway/GEOAPI.Gateway.csproj", "src/GEOAPI.Gateway/"]
COPY ["src/GEOAPI.Application/GEOAPI.Application.csproj", "src/GEOAPI.Application/"]
COPY ["src/GEOAPI.Domain/GEOAPI.Domain.csproj", "src/GEOAPI.Domain/"]
COPY ["src/GEOAPI.Infrastructure/GEOAPI.Infrastructure.csproj", "src/GEOAPI.Infrastructure/"]

RUN dotnet restore "src/GEOAPI.Gateway/GEOAPI.Gateway.csproj"

# Copy source code and build
COPY src/ ./src/
WORKDIR "/src/src/GEOAPI.Gateway"
RUN dotnet build "GEOAPI.Gateway.csproj" -c Release -o /app/build

# ============================================
# Stage 2: Publish
# ============================================
FROM build AS publish
RUN dotnet publish "GEOAPI.Gateway.csproj" \
    -c Release \
    -o /app/publish \
    --no-restore \
    /p:UseAppHost=false

# ============================================
# Stage 3: Runtime
# ============================================
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# Install curl for health checks
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r geoapi && useradd -r -g geoapi geoapi

# Copy published app
COPY --from=publish /app/publish .

# Set ownership
RUN chown -R geoapi:geoapi /app

# Switch to non-root user
USER geoapi

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Entry point
ENTRYPOINT ["dotnet", "GEOAPI.Gateway.dll"]
```

### 2.2 .dockerignore

```
# GEOAPI/.dockerignore

**/.vs
**/.vscode
**/bin
**/obj
**/.git
**/.gitignore
**/docker-compose*.yml
**/Dockerfile*
**/*.md
**/logs
**/node_modules
**/npm-debug.log
**/.DS_Store
**/Thumbs.db
```

### 2.3 Build da Imagem Docker

```bash
# Build image
docker build -t geoapi:latest .

# Tag for registry
docker tag geoapi:latest myregistry.azurecr.io/geoapi:1.0.0
docker tag geoapi:latest myregistry.azurecr.io/geoapi:latest

# Push to registry
docker push myregistry.azurecr.io/geoapi:1.0.0
docker push myregistry.azurecr.io/geoapi:latest
```

### 2.4 Docker Compose (Desenvolvimento Local)

```yaml
# docker-compose.yml

version: '3.8'

services:
  geoapi:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ASPNETCORE_URLS=http://+:8080
      - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;Database=carf_geoapi;Username=postgres;Password=postgres
      - Keycloak__Authority=http://keycloak:8080/auth/realms/carf
    depends_on:
      - postgres
      - keycloak
    networks:
      - carf-network

  postgres:
    image: postgis/postgis:16-3.4
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=carf_geoapi
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - carf-network

  keycloak:
    image: quay.io/keycloak/keycloak:24.0
    ports:
      - "8081:8080"
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
      - KC_DB=postgres
      - KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
      - KC_DB_USERNAME=postgres
      - KC_DB_PASSWORD=postgres
    command: start-dev
    depends_on:
      - postgres
    networks:
      - carf-network

volumes:
  postgres-data:

networks:
  carf-network:
    driver: bridge
```

---

## 3. Orquestração com Kubernetes

### 3.1 Deployment Manifest

```yaml
# k8s/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoapi
  namespace: carf-production
  labels:
    app: geoapi
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: geoapi
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: geoapi
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: geoapi
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: geoapi
        image: myregistry.azurecr.io/geoapi:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        - name: ASPNETCORE_URLS
          value: "http://+:8080"
        - name: ConnectionStrings__DefaultConnection
          valueFrom:
            secretKeyRef:
              name: geoapi-secrets
              key: database-connection-string
        - name: Keycloak__Authority
          valueFrom:
            configMapKeyRef:
              name: geoapi-config
              key: keycloak-authority
        - name: Keycloak__Audience
          value: "geoapi"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 20
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30
        volumeMounts:
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: logs
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - geoapi
              topologyKey: kubernetes.io/hostname
```

### 3.2 Service Manifest

```yaml
# k8s/service.yaml

apiVersion: v1
kind: Service
metadata:
  name: geoapi
  namespace: carf-production
  labels:
    app: geoapi
spec:
  type: ClusterIP
  selector:
    app: geoapi
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None
```

### 3.3 Ingress Manifest

```yaml
# k8s/ingress.yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: geoapi
  namespace: carf-production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://geoweb.carf.gov.br,https://admin.carf.gov.br"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
    nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization, Content-Type"
spec:
  tls:
  - hosts:
    - api.carf.gov.br
    secretName: geoapi-tls
  rules:
  - host: api.carf.gov.br
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: geoapi
            port:
              name: http
```

### 3.4 ConfigMap

```yaml
# k8s/configmap.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: geoapi-config
  namespace: carf-production
data:
  keycloak-authority: "https://auth.carf.gov.br/auth/realms/carf"
  elasticsearch-uri: "https://logs.carf.gov.br"
  serilog-minimum-level: "Information"
  cors-allowed-origins: "https://geoweb.carf.gov.br,https://admin.carf.gov.br,https://geogis.carf.gov.br"
```

### 3.5 Secrets (exemplo - não commitar valores reais)

```yaml
# k8s/secrets.yaml

apiVersion: v1
kind: Secret
metadata:
  name: geoapi-secrets
  namespace: carf-production
type: Opaque
stringData:
  database-connection-string: "Host=postgres.carf-production.svc.cluster.local;Port=5432;Database=carf_geoapi;Username=geoapi_user;Password=${DB_PASSWORD};SSL Mode=Require"
  smtp-password: "${SMTP_PASSWORD}"
  sms-api-key: "${SMS_API_KEY}"
  aws-access-key: "${AWS_ACCESS_KEY}"
  aws-secret-key: "${AWS_SECRET_KEY}"
```

**Nota:** Em produção, usar Azure Key Vault Secrets Provider ou similar:

```yaml
# k8s/secret-provider-class.yaml

apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: geoapi-keyvault
  namespace: carf-production
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "${USER_ASSIGNED_IDENTITY_CLIENT_ID}"
    keyvaultName: "carf-keyvault"
    objects: |
      array:
        - |
          objectName: database-password
          objectType: secret
          objectVersion: ""
        - |
          objectName: smtp-password
          objectType: secret
          objectVersion: ""
    tenantId: "${AZURE_TENANT_ID}"
```

### 3.6 HorizontalPodAutoscaler (HPA)

```yaml
# k8s/hpa.yaml

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: geoapi
  namespace: carf-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: geoapi
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

### 3.7 PodDisruptionBudget (PDB)

```yaml
# k8s/pdb.yaml

apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: geoapi
  namespace: carf-production
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: geoapi
```

### 3.8 NetworkPolicy

```yaml
# k8s/network-policy.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: geoapi
  namespace: carf-production
spec:
  podSelector:
    matchLabels:
      app: geoapi
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  # Allow PostgreSQL
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  # Allow Keycloak
  - to:
    - podSelector:
        matchLabels:
          app: keycloak
    ports:
    - protocol: TCP
      port: 8080
  # Allow external HTTPS (for Keycloak, Email, SMS)
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

---

## 4. CI/CD Pipeline

### 4.1 GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml

name: CI/CD - GEOAPI

on:
  push:
    branches:
      - main
      - develop
    paths:
      - 'PROJECTS/GEOAPI/SRC-CODE/**'
      - '.github/workflows/deploy.yml'
  pull_request:
    branches:
      - main
      - develop

env:
  REGISTRY: myregistry.azurecr.io
  IMAGE_NAME: geoapi
  DOTNET_VERSION: '9.0.x'

jobs:
  # ============================================
  # Job 1: Build and Test
  # ============================================
  build-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: PROJECTS/GEOAPI/SRC-CODE

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{ env.DOTNET_VERSION }}

    - name: Restore dependencies
      run: dotnet restore

    - name: Build
      run: dotnet build --configuration Release --no-restore

    - name: Run unit tests
      run: dotnet test --configuration Release --no-build --verbosity normal --collect:"XPlat Code Coverage"

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./**/coverage.cobertura.xml
        flags: unittests
        name: codecov-geoapi

    - name: Run integration tests
      run: |
        docker-compose -f docker-compose.test.yml up -d
        dotnet test tests/GEOAPI.IntegrationTests --configuration Release --no-build
        docker-compose -f docker-compose.test.yml down

  # ============================================
  # Job 2: Security Scan
  # ============================================
  security-scan:
    runs-on: ubuntu-latest
    needs: build-and-test

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: 'PROJECTS/GEOAPI/SRC-CODE'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  # ============================================
  # Job 3: Build and Push Docker Image
  # ============================================
  build-and-push-image:
    runs-on: ubuntu-latest
    needs: [build-and-test, security-scan]
    if: github.event_name == 'push'

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: PROJECTS/GEOAPI/SRC-CODE
        file: PROJECTS/GEOAPI/SRC-CODE/Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Scan Docker image with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-image-results.sarif'

  # ============================================
  # Job 4: Deploy to Staging
  # ============================================
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push-image
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://api-staging.carf.gov.br

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Set AKS context
      uses: azure/aks-set-context@v3
      with:
        resource-group: carf-staging-rg
        cluster-name: carf-staging-aks

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/geoapi \
          geoapi=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n carf-staging

        kubectl rollout status deployment/geoapi -n carf-staging --timeout=5m

    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://api-staging.carf.gov.br/health || exit 1

  # ============================================
  # Job 5: Deploy to Production
  # ============================================
  deploy-production:
    runs-on: ubuntu-latest
    needs: build-and-push-image
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://api.carf.gov.br

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Set AKS context
      uses: azure/aks-set-context@v3
      with:
        resource-group: carf-production-rg
        cluster-name: carf-production-aks

    - name: Deploy to Kubernetes (Blue-Green)
      run: |
        # Create new deployment (green)
        kubectl apply -f k8s/deployment-green.yaml -n carf-production

        # Wait for green to be ready
        kubectl rollout status deployment/geoapi-green -n carf-production --timeout=10m

        # Switch traffic to green
        kubectl patch service geoapi \
          -p '{"spec":{"selector":{"version":"green"}}}' \
          -n carf-production

        # Wait and verify
        sleep 60
        curl -f https://api.carf.gov.br/health || exit 1

        # Delete old blue deployment
        kubectl delete deployment geoapi-blue -n carf-production --ignore-not-found

    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'GEOAPI deployed to production 🚀'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      if: always()
```

### 4.2 Database Migration Job

```yaml
# .github/workflows/db-migration.yml

name: Database Migration

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '9.0.x'

    - name: Install EF Core tools
      run: dotnet tool install --global dotnet-ef

    - name: Run migrations
      env:
        CONNECTION_STRING: ${{ secrets.DATABASE_CONNECTION_STRING }}
      run: |
        cd PROJECTS/GEOAPI/SRC-CODE/src/GEOAPI.Infrastructure
        dotnet ef database update --connection "$CONNECTION_STRING" --verbose
```

---

## 5. Estratégia Multi-Ambiente

### 5.1 Ambientes

| Ambiente | URL | Cluster | Replicas | Purpose |
|----------|-----|---------|----------|---------|
| **Development** | localhost | Docker Compose | 1 | Desenvolvimento local |
| **Staging** | api-staging.carf.gov.br | AKS Staging | 2 | Testes de integração |
| **Production** | api.carf.gov.br | AKS Production | 3-10 (HPA) | Produção |

### 5.2 Configuração por Ambiente

**Development (appsettings.Development.json):**
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft": "Information"
    },
    "EnableSensitiveDataLogging": true
  },
  "Keycloak": {
    "Authority": "http://localhost:8081/auth/realms/carf",
    "RequireHttpsMetadata": false
  },
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=carf_geoapi_dev;Username=postgres;Password=postgres"
  }
}
```

**Staging (appsettings.Staging.json):**
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "Keycloak": {
    "Authority": "https://auth-staging.carf.gov.br/auth/realms/carf",
    "RequireHttpsMetadata": true
  },
  "ConnectionStrings": {
    "DefaultConnection": "${DATABASE_CONNECTION_STRING}"
  }
}
```

**Production (appsettings.Production.json):**
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft": "Error"
    }
  },
  "Keycloak": {
    "Authority": "https://auth.carf.gov.br/auth/realms/carf",
    "RequireHttpsMetadata": true,
    "ValidateLifetime": true
  },
  "ConnectionStrings": {
    "DefaultConnection": "${DATABASE_CONNECTION_STRING}"
  }
}
```

### 5.3 Feature Flags

```csharp
// GEOAPI/src/Gateway/Program.cs

using Microsoft.FeatureManagement;

builder.Services.AddFeatureManagement(builder.Configuration.GetSection("FeatureFlags"));

// appsettings.json
{
  "FeatureFlags": {
    "EnableNewUnitValidation": false,
    "EnableAdvancedSearch": true,
    "EnableEmailNotifications": true
  }
}

// Usage in controller
[ApiController]
[Route("api/v1/[controller]")]
public class UnitsController : ControllerBase
{
    private readonly IFeatureManager _featureManager;

    [HttpPost]
    public async Task<ActionResult> CreateUnit([FromBody] CreateUnitDto dto)
    {
        if (await _featureManager.IsEnabledAsync("EnableNewUnitValidation"))
        {
            // New validation logic
        }
        else
        {
            // Old validation logic
        }
    }
}
```

---

## 6. Configuração e Secrets

### 6.1 Hierarquia de Configuração

```
1. appsettings.json (base configuration)
2. appsettings.{Environment}.json (environment-specific)
3. Environment Variables (K8s ConfigMap/Secrets)
4. Azure Key Vault (production secrets)
5. Command-line arguments (overrides)
```

### 6.2 Azure Key Vault Integration

```csharp
// GEOAPI/src/Gateway/Program.cs

using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var builder = WebApplication.CreateBuilder(args);

if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:VaultUri"]!);
    var credential = new DefaultAzureCredential();

    builder.Configuration.AddAzureKeyVault(keyVaultUri, credential);
}

// Access secrets
var dbPassword = builder.Configuration["database-password"];
var smtpPassword = builder.Configuration["smtp-password"];
```

### 6.3 Secrets Rotation

```bash
# Rotate database password
# 1. Generate new password
NEW_PASSWORD=$(openssl rand -base64 32)

# 2. Update Key Vault
az keyvault secret set \
  --vault-name carf-keyvault \
  --name database-password \
  --value "$NEW_PASSWORD"

# 3. Update database user password
psql -h postgres.carf.gov.br -U admin -c "ALTER USER geoapi_user WITH PASSWORD '$NEW_PASSWORD';"

# 4. Restart pods to pick up new secret
kubectl rollout restart deployment/geoapi -n carf-production
```

---

## 7. Monitoramento e Observabilidade

### 7.1 Prometheus Metrics

```csharp
// Already configured in previous documents (MetricsService)
// Prometheus scrapes /metrics endpoint
```

**Prometheus Configuration (prometheus.yml):**
```yaml
scrape_configs:
  - job_name: 'geoapi'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - carf-production
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

### 7.2 Grafana Dashboards

**Key Metrics Dashboard:**
- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate (%)
- Active connections
- Database query duration
- Memory/CPU usage
- Pod count (HPA)

**Example PromQL Queries:**
```promql
# Request rate
rate(geoapi_http_requests_total[5m])

# Average response time
rate(geoapi_http_request_duration_seconds_sum[5m]) / rate(geoapi_http_request_duration_seconds_count[5m])

# Error rate
rate(geoapi_http_requests_total{status=~"5.."}[5m]) / rate(geoapi_http_requests_total[5m])

# Database query duration P95
histogram_quantile(0.95, rate(geoapi_database_query_duration_seconds_bucket[5m]))
```

### 7.3 Elasticsearch + Kibana (Logging)

**Fluent Bit DaemonSet (sends logs to Elasticsearch):**
```yaml
# k8s/fluent-bit.yaml

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluent-bit
  template:
    metadata:
      labels:
        app: fluent-bit
    spec:
      serviceAccountName: fluent-bit
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:2.0
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc/
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluent-bit-config
        configMap:
          name: fluent-bit-config
```

### 7.4 Distributed Tracing (Application Insights / Jaeger)

```csharp
// GEOAPI/src/Gateway/Program.cs

using Azure.Monitor.OpenTelemetry.AspNetCore;

builder.Services.AddOpenTelemetry()
    .WithTracing(tracerProviderBuilder =>
    {
        tracerProviderBuilder
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddEntityFrameworkCoreInstrumentation()
            .AddSource("GEOAPI.*");

        if (builder.Environment.IsProduction())
        {
            tracerProviderBuilder.AddAzureMonitorTraceExporter(options =>
            {
                options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
            });
        }
        else
        {
            tracerProviderBuilder.AddJaegerExporter(options =>
            {
                options.AgentHost = "jaeger";
                options.AgentPort = 6831;
            });
        }
    });
```

### 7.5 Alerting Rules (Prometheus Alertmanager)

```yaml
# alerting-rules.yaml

groups:
  - name: geoapi
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(geoapi_http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # High response time
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(geoapi_http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "P95 response time is {{ $value }}s (threshold: 2s)"

      # Pod down
      - alert: PodDown
        expr: kube_deployment_status_replicas_available{deployment="geoapi"} < 2
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "GEOAPI pods are down"
          description: "Only {{ $value }} pods available (minimum: 2)"

      # Database connection issues
      - alert: DatabaseConnectionFailure
        expr: rate(geoapi_database_queries_total{status="error"}[5m]) > 0.1
        for: 3m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failures detected"
          description: "Database error rate: {{ $value | humanizePercentage }}"
```

---

## 8. Backup e Disaster Recovery

### 8.1 PostgreSQL Backup Strategy

**CronJob para backup automático:**
```yaml
# k8s/postgres-backup-cronjob.yaml

apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: carf-production
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:16
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secrets
                  key: password
            - name: PGHOST
              value: "postgres.carf-production.svc.cluster.local"
            - name: PGUSER
              value: "postgres"
            - name: PGDATABASE
              value: "carf_geoapi"
            - name: BACKUP_RETENTION_DAYS
              value: "30"
            command:
            - /bin/bash
            - -c
            - |
              TIMESTAMP=$(date +%Y%m%d_%H%M%S)
              BACKUP_FILE="/backups/geoapi_${TIMESTAMP}.sql.gz"

              # Create backup
              pg_dump -Fc -Z9 | gzip > "$BACKUP_FILE"

              # Upload to Azure Blob Storage
              az storage blob upload \
                --account-name carfbackups \
                --container-name postgres-backups \
                --name "geoapi_${TIMESTAMP}.sql.gz" \
                --file "$BACKUP_FILE"

              # Delete old backups
              find /backups -name "geoapi_*.sql.gz" -mtime +${BACKUP_RETENTION_DAYS} -delete
            volumeMounts:
            - name: backups
              mountPath: /backups
          volumes:
          - name: backups
            persistentVolumeClaim:
              claimName: postgres-backups
          restartPolicy: OnFailure
```

### 8.2 Restore Procedure

```bash
# Download backup from Azure Blob Storage
az storage blob download \
  --account-name carfbackups \
  --container-name postgres-backups \
  --name "geoapi_20260109_120000.sql.gz" \
  --file "./backup.sql.gz"

# Restore backup
gunzip -c backup.sql.gz | psql -h postgres.carf.gov.br -U postgres -d carf_geoapi
```

### 8.3 Disaster Recovery Plan

**Recovery Time Objective (RTO):** 1 hora
**Recovery Point Objective (RPO):** 6 horas (intervalo de backup)

**Procedimento:**
1. Provisionar novo cluster Kubernetes (se necessário)
2. Restaurar banco de dados do backup mais recente
3. Deploy da última versão estável do GEOAPI
4. Atualizar DNS para novo cluster
5. Verificar health checks
6. Notificar stakeholders

---

## 9. Segurança no Deployment

### 9.1 Image Scanning

```yaml
# Trivy scan in CI/CD (already shown above)
- name: Scan Docker image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
    format: 'table'
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

### 9.2 Pod Security Standards

```yaml
# k8s/pod-security-policy.yaml

apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: false
```

### 9.3 Network Policies (já mostrado acima)

### 9.4 RBAC (Role-Based Access Control)

```yaml
# k8s/rbac.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: geoapi
  namespace: carf-production

---

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: geoapi
  namespace: carf-production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]

---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: geoapi
  namespace: carf-production
subjects:
- kind: ServiceAccount
  name: geoapi
  namespace: carf-production
roleRef:
  kind: Role
  name: geoapi
  apiGroup: rbac.authorization.k8s.io
```

### 9.5 TLS/SSL Configuration

**cert-manager para certificados Let's Encrypt:**
```yaml
# k8s/cert-manager-issuer.yaml

apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@carf.gov.br
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Ingress com TLS (já mostrado acima)**

---

## 📚 Referências

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Trivy Security Scanner](https://aquasecurity.github.io/trivy/)

---

## 🔗 Documentos Relacionados

- [01-overview.md](./01-overview.md) - Visão geral da arquitetura
- [02-admin-security.md](./02-admin-security.md) - Segurança e separação admin
- [03-data-flow.md](./03-data-flow.md) - Fluxo de dados
- [04-integration.md](./04-integration.md) - Integrações externas
- [HOW-TO/01-setup-dev-environment.md](../HOW-TO/01-setup-dev-environment.md) - Setup de desenvolvimento
- [HOW-TO/02-build-and-run.md](../HOW-TO/02-build-and-run.md) - Build e execução
