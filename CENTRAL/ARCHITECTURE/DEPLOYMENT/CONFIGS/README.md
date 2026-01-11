# CONFIGS

Arquivos de configuração deployment do CARF. nginx.conf para GEOWEB (server listen 80, root /usr/share/nginx/html, try_files SPA routing, gzip compression, caching headers static assets, proxy_pass /api para GEOAPI upstream, CORS headers, security headers X-Frame-Options/CSP). env-vars.md documenta variáveis ambiente por projeto (GEOAPI: DATABASE_URL, KEYCLOAK_URL, REDIS_URL, JWT_SECRET, LOG_LEVEL; GEOWEB: VITE_API_URL, VITE_KEYCLOAK_URL; REURBCAD: API_URL, SYNC_INTERVAL). health-checks.md especifica endpoints (GEOAPI /health retorna 200 + JSON status db/redis, /ready retorna 200 apenas se dependencies ok, PostgreSQL pg_isready, Keycloak /health).

## Documentação

- **[env-vars.md](./env-vars.md)** - Variáveis de ambiente obrigatórias/opcionais por projeto (GEOAPI, GEOWEB, REURBCAD, KEYCLOAK)
- **[health-checks.md](./health-checks.md)** - Endpoints de health check e readiness probes (/health, /ready)

---

**Última atualização:** 2025-12-29
