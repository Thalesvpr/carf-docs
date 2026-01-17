# DOCKERFILES

Projeto CARF utiliza Dockerfiles otimizados para build eficiente e seguro de cada componente do sistema seguindo Docker best practices como multi-stage builds layer caching e minimal runtime images reduzindo tamanho final e superfície de ataque.

Backend GEOAPI implementa Dockerfile.geoapi com multi-stage build dividido em stage 1 restore dependencies executando dotnet restore com layer caching permitindo rebuild rápido quando apenas código-fonte muda sem dependencies alteradas, stage 2 build compilando aplicação com dotnet build em modo Release, stage 3 publish gerando release artifacts com dotnet publish otimizações AOT trimming unused assemblies, stage 4 runtime usando base image aspnet:8.0 slim copiando apenas binários publicados sem SDK completo minimizando image size de 1GB para 200MB melhorando tempo de pull e deploy.

Frontend GEOWEB usa Dockerfile.geoweb FROM node:20-alpine copiando package.json e package-lock.json primeiro executando npm ci com production only flag instalando exact versions sem devDependencies, COPY src copiando código-fonte após dependencies para layer caching eficiente, RUN npm build gerando static assets otimizados Vite com minificação tree-shaking code splitting, seguido por multi-stage FROM nginx:alpine servindo static files com nginx.conf customizado incluindo gzip compression cache headers try_files para SPA routing e proxy_pass para backend API.

Database PostgreSQL customizado via Dockerfile.postgres FROM postgis/postgis:16-3.4 base image oficial incluindo extensão PostGIS para spatial queries, COPY init-scripts/ executados automaticamente via /docker-entrypoint-initdb.d criando extensions schemas RLS policies e seed data inicial garantindo database pronto para uso após primeiro startup.

Instruções HEALTHCHECK adicionadas em cada Dockerfile para integração com Docker Compose e Kubernetes sendo GEOAPI curl http://localhost:8080/health validando API responding corretamente, PostgreSQL pg_isready validando database aceitando connections. Todos containers executam como non-root USER após setup inicial seguindo security principle of least privilege prevenindo privilege escalation attacks caso container seja comprometido. Arquivo .dockerignore excluindo node_modules/ bin/ obj/ .git reduzindo build context enviado para Docker daemon acelerando builds e evitando leak de arquivos sensíveis em layers intermediárias.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

