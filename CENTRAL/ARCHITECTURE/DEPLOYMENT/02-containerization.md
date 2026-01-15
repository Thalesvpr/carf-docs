# Containerization

Containerização Docker do CARF garantindo portabilidade entre ambientes cloud e on-premises conforme ADR-020. GEOAPI Dockerfile multi-stage (build stage compilando .NET conforme ADR-001, runtime stage com imagem slim aspnet) otimizado para cache layers (COPY *.csproj primeiro, depois dotnet restore, finalmente COPY código), resultando em imagem ~200MB. GEOWEB Dockerfile usando Node Alpine (build Vite SPA conforme ADR-012, nginx serving static files), compressão brotli habilitada, resultando em imagem ~50MB. REURBCAD build separado (bundles iOS/Android via Expo EAS não containerizado conforme ADR-004), sync service backend containerizado Node Alpine. GEOGIS distribuído como Python package wheel não containerizado (instalação direta em QGIS). Docker Compose orquestrando stack local dev (postgres PostGIS conforme ADR-002, keycloak conforme ADR-003, redis, rabbitmq, geoapi, geoweb) com volumes persistentes, networks isoladas, healthchecks garantindo ordem inicialização, e hot reload habilitado para dev experience. Registry privado (AWS ECR, Azure ACR, ou Harbor on-premises) armazenando imagens tagged (v1.2.3, latest, sha-abc123) com scan automático de vulnerabilidades Trivy bloqueando push de imagens high/critical, retention policy deletando tags antigas após 90 dias, e replicação cross-region para disaster recovery.

## Projetos Containerizados

Containerização via Docker é aplicada em com multi-stage build otimizado para .NET 9 gerando imagem final slim, usando imagem oficial Keycloak customizada com temas CARF empacotados, e PostgreSQL+PostGIS para banco de dados geográfico com persistent volumes garantindo durabilidade, todos orquestrados via Docker Compose em dev e Kubernetes em prod com manifests em DEPLOYMENT/CONFIGS/, enquanto e usam Vercel (ADR-013) serverless sem necessidade de containers.

---

**Última atualização:** 2026-01-10
**Status do arquivo**: Pronto
