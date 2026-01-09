# Containerization

Containerização Docker do CARF garantindo portabilidade entre ambientes cloud e on-premises. GEOAPI Dockerfile multi-stage (build stage compilando .NET, runtime stage com imagem slim aspnet) otimizado para cache layers (COPY *.csproj primeiro, depois dotnet restore, finalmente COPY código), resultando em imagem ~200MB. GEOWEB Dockerfile usando Node Alpine (build Vite SPA, nginx serving static files), compressão brotli habilitada, resultando em imagem ~50MB. REURBCAD build separado (bundles iOS/Android via Expo EAS não containerizado), sync service backend containerizado Node Alpine. GEOGIS distribuído como Python package wheel não containerizado (instalação direta em QGIS). Docker Compose orquestrando stack local dev (postgres, keycloak, redis, rabbitmq, geoapi, geoweb) com volumes persistentes, networks isoladas, healthchecks garantindo ordem inicialização, e hot reload habilitado para dev experience. Registry privado (AWS ECR, Azure ACR, ou Harbor on-premises) armazenando imagens tagged (v1.2.3, latest, sha-abc123) com scan automático de vulnerabilidades Trivy bloqueando push de imagens high/critical, retention policy deletando tags antigas após 90 dias, e replicação cross-region para disaster recovery.

---

**Última atualização:** 2025-12-30
