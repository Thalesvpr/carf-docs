# Configurar Ambiente de Produção

**Nível**: Avançado | **Tempo**: 4-6 horas

## 1. PostgreSQL Externo

### AWS RDS
```bash
# Create RDS PostgreSQL 16
aws rds create-db-instance \
  --db-instance-identifier carf-keycloak-prod \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 16 \
  --master-username keycloak \
  --master-user-password <strong-password> \
  --allocated-storage 100 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name carf-db-subnet

# Update env vars
KC_DB_URL=jdbc:postgresql://carf-keycloak-prod.xxx.rds.amazonaws.com:5432/keycloak
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=<password>
```

## 2. HTTPS/TLS

### Via Load Balancer (recomendado)
```yaml
# Kubernetes Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: keycloak-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - keycloak.carf.gov.br
    secretName: keycloak-tls
  rules:
  - host: keycloak.carf.gov.br
    http:
      paths:
      - path: /
        backend:
          service:
            name: keycloak
            port:
              number: 8080
```

### Via Keycloak (alternativo)
```bash
KC_HTTPS_CERTIFICATE_FILE=/opt/keycloak/conf/cert.pem
KC_HTTPS_CERTIFICATE_KEY_FILE=/opt/keycloak/conf/key.pem
KC_HTTPS_PORT=8443
KC_HTTP_ENABLED=false
```

## 3. Resource Limits

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: keycloak
        image: carf/keycloak:1.0.0
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### JVM Heap
```bash
JAVA_OPTS="-Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=512m"
```

## 4. Clustering (High Availability)

```bash
# Enable Infinispan clustering
KC_CACHE=ispn
KC_CACHE_STACK=kubernetes

# Kubernetes deployment com 3+ replicas
kubectl scale deployment/keycloak --replicas=3
```

## 5. Performance Tuning

### Database Connection Pool
```bash
KC_DB_POOL_INITIAL_SIZE=10
KC_DB_POOL_MIN_SIZE=10
KC_DB_POOL_MAX_SIZE=50
KC_TRANSACTION_XA_ENABLED=false
```

### Cache
```bash
KC_CACHE_CONFIG_FILE=/opt/keycloak/conf/cache-ispn.xml
```

## 6. Backup Strategy

### Automated Daily Backups
```bash
# Cron job
0 2 * * * /opt/keycloak/scripts/backup.sh

# Upload to S3
aws s3 cp /opt/keycloak/backups/ s3://carf-backups/keycloak/ --recursive
```

### Retention Policy
- Daily: 7 dias
- Weekly: 4 semanas
- Monthly: 12 meses

## 7. Monitoring

### Prometheus
```yaml
# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: keycloak
spec:
  selector:
    matchLabels:
      app: keycloak
  endpoints:
  - port: http
    path: /metrics
```

### Grafana Dashboard
```bash
# Import dashboard
https://grafana.com/grafana/dashboards/10441
```

### Alerts
```yaml
groups:
- name: keycloak
  rules:
  - alert: KeycloakDown
    expr: up{job="keycloak"} == 0
    for: 2m
  - alert: HighLoginErrors
    expr: rate(keycloak_login_errors_total[5m]) > 10
    for: 5m
```

## 8. Logging

```bash
# Structured JSON logs
KC_LOG_FORMAT=json
KC_LOG_LEVEL=info

# Ship to ELK/CloudWatch
fluentd → elasticsearch
```

## 9. Security

### Secrets Management
```bash
# AWS Secrets Manager
aws secretsmanager create-secret --name keycloak-db-password
aws secretsmanager create-secret --name keycloak-admin-password

# Kubernetes External Secrets
kubectl apply -f external-secrets.yaml
```

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: keycloak-netpol
spec:
  podSelector:
    matchLabels:
      app: keycloak
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8080
```

## 10. Disaster Recovery

```bash
# 1. Backup em região secundária
aws s3 sync s3://carf-backups-us-east-1/keycloak/ s3://carf-backups-eu-west-1/keycloak/

# 2. Standby cluster em região secundária
kubectl config use-context eu-west-1
kubectl apply -f keycloak-deployment.yaml

# 3. DNS failover (Route53)
aws route53 change-resource-record-sets --hosted-zone-id Z123 --change-batch file://failover.json
```

## Checklist Produção

- [ ] PostgreSQL RDS configurado com multi-AZ
- [ ] HTTPS/TLS via Load Balancer
- [ ] Resource limits definidos (CPU/memory)
- [ ] Clustering habilitado (3+ replicas)
- [ ] Connection pool otimizado
- [ ] Backup diário automatizado + S3
- [ ] Prometheus + Grafana configurados
- [ ] Alertas críticos ativos
- [ ] Logs centralizados (ELK/CloudWatch)
- [ ] Secrets via Secrets Manager
- [ ] Network policies aplicadas
- [ ] DR plan testado
