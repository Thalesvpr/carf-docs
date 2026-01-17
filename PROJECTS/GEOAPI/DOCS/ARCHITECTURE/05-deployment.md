# Deployment

GEOAPI deployment usa containerização Docker com orquestração Kubernetes para ambientes staging e produção. Dockerfile multi-stage com build stage SDK compilando publicando e runtime stage ASP.NET runtime copiando artefatos, imagem final aproximadamente 200MB com healthcheck endpoint /health.

Kubernetes deployment configura replicas 3 produção com resource requests memory 512Mi cpu 250m limits memory 1Gi cpu 500m, liveness probe /health/live readiness probe /health/ready com initial delay 10s period 30s, environment variables via ConfigMap para não sensíveis e Secrets para connection strings JWT keys, horizontal pod autoscaler escala 3-10 replicas baseado CPU 70% ou custom metrics requests por segundo.

Ambientes incluem development local Docker Compose com PostgreSQL Keycloak GEOAPI hot reload, staging cluster Kubernetes namespace staging com dados anonimizados para testes integração, e production cluster Kubernetes namespace production com alta disponibilidade backups automáticos monitoring alertas.

CI/CD pipeline GitHub Actions executa build test push deploy onde push main branch triggera workflow, build step compila .NET 9 executa unit tests gera coverage report, Docker step builda imagem tageia com git sha e latest push para container registry, deploy step usa kubectl set image para rolling update zero downtime com rollback automático se readiness probe falha.

Database migrations executam via Job Kubernetes antes deployment aplicação onde init container aguarda PostgreSQL healthy, migration job executa dotnet ef database update aplicando pending migrations, deployment principal só inicia após migration job completar com sucesso, rollback manual via dotnet ef database update PreviousMigration se necessário.

Monitoring Prometheus scrape /metrics endpoint coletando request duration request count error rate, Grafana dashboards visualizam métricas com alertas Slack quando error rate acima 1% ou latency p99 acima 500ms, logs estruturados JSON via Serilog enviados para Elasticsearch consultáveis via Kibana com correlation id rastreando request através de serviços.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
