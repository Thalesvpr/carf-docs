# DOCKERFILES

Dockerfiles otimizados do CARF. Dockerfile.geoapi multi-stage (stage 1 restore dependencies layer cached, stage 2 build, stage 3 publish release, stage 4 runtime aspnet:8.0 apenas binários minimizando image size). Dockerfile.geoweb (FROM node:20-alpine, COPY package*.json, RUN npm ci production only, COPY src, RUN npm build, FROM nginx:alpine servir static com nginx.conf custom). Dockerfile.postgres (FROM postgis/postgis:16-3.4, COPY init-scripts/ criando extensions/schemas/RLS policies). Health checks via HEALTHCHECK instruction (GEOAPI curl /health, PostgreSQL pg_isready). Non-root USER para segurança. .dockerignore excluindo node_modules/, bin/, obj/.

---

**Última atualização:** 2025-12-29
