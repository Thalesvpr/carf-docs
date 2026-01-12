# Configurar Ambiente de Produção

Configuração ambiente produção Keycloak nível avançado requer 4-6 horas cobrindo infraestrutura completa. PostgreSQL externo via AWS RDS criando db-instance-identifier carf-keycloak-prod, db-instance-class db.t3.medium, engine postgres version 16, master-username keycloak, allocated-storage 100, vpc-security-group-ids e db-subnet-group-name apropriados, environment vars KC_DB_URL=jdbc:postgresql://carf-keycloak-prod.xxx.rds.amazonaws.com:5432/keycloak KC_DB_USERNAME=keycloak KC_DB_PASSWORD com strong password.

HTTPS/TLS via Load Balancer recomendado usando Kubernetes Ingress com cert-manager.io/cluster-issuer letsencrypt-prod, spec tls hosts keycloak.carf.gov.br secretName keycloak-tls, rules http paths backend service keycloak port 8080. Alternativa via Keycloak direto configurando KC_HTTPS_CERTIFICATE_FILE=/opt/keycloak/conf/cert.pem KC_HTTPS_CERTIFICATE_KEY_FILE=/opt/keycloak/conf/key.pem KC_HTTPS_PORT=8443 KC_HTTP_ENABLED=false.

Resource limits Kubernetes Deployment replicas 3, containers resources requests memory 1Gi cpu 500m limits memory 2Gi cpu 1000m, JVM Heap JAVA_OPTS -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=512m. Clustering High Availability habilitando Infinispan KC_CACHE=ispn KC_CACHE_STACK=kubernetes, kubectl scale deployment/keycloak --replicas=3.

Performance tuning Database Connection Pool KC_DB_POOL_INITIAL_SIZE=10 KC_DB_POOL_MIN_SIZE=10 KC_DB_POOL_MAX_SIZE=50 KC_TRANSACTION_XA_ENABLED=false, cache config KC_CACHE_CONFIG_FILE=/opt/keycloak/conf/cache-ispn.xml.

Backup strategy automated daily via cron job 0 2 * * * /opt/keycloak/scripts/backup.sh, upload S3 aws s3 cp /opt/keycloak/backups/ s3://carf-backups/keycloak/ --recursive, retention policy daily 7 dias weekly 4 semanas monthly 12 meses.

Monitoring Prometheus via ServiceMonitor selector matchLabels app keycloak endpoints port http path /metrics, Grafana Dashboard importando https://grafana.com/grafana/dashboards/10441, Alerts groups keycloak rules KeycloakDown expr up job=keycloak == 0 for 2m e HighLoginErrors expr rate keycloak_login_errors_total 5m maior 10 for 5m.

Logging structured JSON KC_LOG_FORMAT=json KC_LOG_LEVEL=info, ship para ELK/CloudWatch via fluentd elasticsearch. Security Secrets Management via AWS Secrets Manager create-secret keycloak-db-password keycloak-admin-password, Kubernetes External Secrets kubectl apply -f external-secrets.yaml, Network Policies NetworkPolicy keycloak-netpol podSelector app keycloak ingress from podSelector app nginx-ingress ports TCP 8080.

Disaster Recovery backup região secundária aws s3 sync us-east-1 para eu-west-1, standby cluster região secundária kubectl config use-context eu-west-1 kubectl apply keycloak-deployment.yaml, DNS failover Route53 change-resource-record-sets hosted-zone-id change-batch failover.json.

Checklist produção PostgreSQL RDS multi-AZ, HTTPS/TLS Load Balancer, resource limits CPU memory, clustering 3+ replicas, connection pool otimizado, backup diário S3, Prometheus Grafana, alertas críticos ativos, logs centralizados ELK/CloudWatch, secrets via Secrets Manager, network policies aplicadas, DR plan testado.

---

**Última atualização:** 2026-01-12
