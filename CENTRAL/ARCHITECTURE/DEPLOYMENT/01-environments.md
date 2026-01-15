# Environments

Ambientes separados do CARF (dev, staging, prod) com configurações isoladas garantindo progressão controlada de releases conforme ADR-020 orquestrando deployments. Dev ambiente para desenvolvimento contínuo com deploy automático em push main branch, dados sintéticos resetáveis, feature flags habilitadas por padrão, logs debug verbosos, e SSL self-signed. Staging ambiente pré-produção espelhando prod com dados anonimizados de produção, deploy manual após approval QA, smoke tests automatizados validando funcionalidades críticas, e SSL válido wildcard. Prod ambiente produção com deploy blue-green zero-downtime, dados reais multi-tenant isolados via RLS conforme ADR-005, monitoramento 24/7 Prometheus/Grafana, backups automáticos cross-region, SSL Let's Encrypt auto-renovado, e rollback automático se healthcheck falhar. Configurações gerenciadas via environment variables (DATABASE_URL, KEYCLOAK_REALM_URL, JWT_SECRET_KEY, REDIS_URL, RABBITMQ_URL) injetadas via Kubernetes ConfigMaps/Secrets ou .env files local, jamais hardcoded no código, versionadas separadamente por ambiente em repositório privado infra configs, e validadas em startup falhando fast se obrigatórias faltarem.

## Projetos Deployados Nestes Ambientes

Todos os projetos CARF seguem estratégia tri-ambiente (Dev/Staging/Prod) documentada aqui, com implementação específica por projeto em para backend .NET hospedado em Kubernetes cluster gerenciado executando pods com HPA horizontal scaling, para frontend React Vite deployado via Vercel (ADR-013) com preview deploys automáticos em PRs, para mobile React Native com EAS builds distribuindo via App Store Google Play com environment-specific configs, para auth provider multi-tenant com realm por município segregando users via multi-tenancy RLS (ADR-005), para site estático Astro Starlight servido via Vercel CDN com builds rápidos conforme ADR-016, e para console administrativo Next.js com server-side rendering.

---

**Última atualização:** 2026-01-10
**Status do arquivo**: Pronto
