# Environments

Ambientes separados do CARF (dev, staging, prod) com configurações isoladas garantindo progressão controlada de releases. Dev ambiente para desenvolvimento contínuo com deploy automático em push main, dados sintéticos resetáveis, feature flags habilitadas por padrão, logs debug verbosos, e SSL self-signed. Staging ambiente pré-produção espelhando prod com dados anonimizados de produção, deploy manual após approval QA, smoke tests automatizados validando funcionalidades críticas, e SSL válido wildcard. Prod ambiente produção com deploy blue-green zero-downtime, dados reais multi-tenant isolados via RLS, monitoramento 24/7 Prometheus/Grafana, backups automáticos cross-region, SSL Let's Encrypt auto-renovado, e rollback automático se healthcheck falhar. Configurações gerenciadas via environment variables (DATABASE_URL, KEYCLOAK_REALM_URL, JWT_SECRET_KEY, REDIS_URL, RABBITMQ_URL) injetadas via Kubernetes ConfigMaps/Secrets ou .env files local, jamais hardcoded no código, versionadas separadamente por ambiente em repositório privado infra configs, e validadas em startup falhando fast se obrigatórias faltarem.

---

**Última atualização:** 2025-12-30
