# Deploy em Produção

Usar `kc.sh start` ao invés de `start-dev`, configurar SSL/TLS com certificado válido via KC_HTTPS_CERTIFICATE_FILE e KC_HTTPS_CERTIFICATE_KEY_FILE ou proxy reverso Nginx/Traefik terminando SSL, database PostgreSQL externo (AWS RDS, Azure Database, GCP Cloud SQL) ao invés de container, alterar TODAS as senhas (admin, db, client secrets) usando secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) ao invés de .env, habilitar HTTPS obrigatório com KC_HTTP_ENABLED=false e sslRequired=external no realm, configurar hostname correto com KC_HOSTNAME=keycloak.carf.example.com e KC_HOSTNAME_STRICT=true, proxy mode edge (KC_PROXY=edge) se Nginx/Traefik na frente, backups automáticos do PostgreSQL diários com retenção 30 dias, horizontal scaling via Kubernetes com 2+ replicas Keycloak + PostgreSQL PgBouncer connection pooling, monitoramento com Prometheus metrics (KC_METRICS_ENABLED=true) + Grafana dashboards + alertas (high CPU, memory, failed logins, database connection pool exhausted), rate limiting no proxy reverso (max 100 req/min por IP pro /token endpoint previne brute force), logs centralizados com Loki/ELK, disaster recovery plan com RTO 4h RPO 1h testado semestralmente, use Kubernetes StatefulSet pra PostgreSQL com PVC, ConfigMaps pra configs não-sensíveis, Secrets pra senhas, Ingress com cert-manager pra SSL automático via Let's Encrypt, HPA (Horizontal Pod Autoscaler) escalando Keycloak baseado em CPU > 70% ou memory > 80%.

---

**Última atualização:** 2026-01-09
**Status do arquivo**: Review
