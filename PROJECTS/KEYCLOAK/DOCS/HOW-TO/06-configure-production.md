---
type: leaf
status: review
description: "Runbook para configuracao do ambiente de producao Keycloak CARF"
updated: 2026-02-08
---

# Configurar Ambiente de Producao

A configuracao do ambiente de producao do Keycloak CARF e um procedimento de nivel avancado que requer entre 4 e 6 horas, cobrindo a infraestrutura completa desde o banco de dados ate o monitoramento.

## PostgreSQL Externo via AWS RDS

O banco de dados de producao e provisionado como instancia AWS RDS com `db-instance-identifier` carf-keycloak-prod, classe `db.t3.medium`, engine PostgreSQL versao 16, usuario master `keycloak` e 100 GB de armazenamento alocado. Os security groups e subnet groups devem ser configurados conforme a topologia da VPC. As variaveis de ambiente do Keycloak apontam para essa instancia com `KC_DB_URL=jdbc:postgresql://carf-keycloak-prod.xxx.rds.amazonaws.com:5432/keycloak`, `KC_DB_USERNAME=keycloak` e `KC_DB_PASSWORD` com uma senha forte.

## HTTPS e TLS

A abordagem recomendada e terminar TLS no Load Balancer usando Kubernetes Ingress com `cert-manager.io/cluster-issuer: letsencrypt-prod`. O Ingress define TLS para o host `keycloak.carf.gov.br` com secret `keycloak-tls`, e as regras de roteamento HTTP direcionam para o servico keycloak na porta 8080. Como alternativa, o TLS pode ser configurado diretamente no Keycloak com `KC_HTTPS_CERTIFICATE_FILE=/opt/keycloak/conf/cert.pem`, `KC_HTTPS_CERTIFICATE_KEY_FILE=/opt/keycloak/conf/key.pem`, `KC_HTTPS_PORT=8443` e `KC_HTTP_ENABLED=false`.

## Resource Limits e JVM

O Deployment Kubernetes deve configurar 3 replicas com resource requests de 1Gi de memoria e 500m de CPU, e limits de 2Gi de memoria e 1000m de CPU. A JVM e configurada via `JAVA_OPTS` com `-Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=512m` para garantir uso previsivel de memoria.

## Clustering e Alta Disponibilidade

O clustering e habilitado via Infinispan com as variaveis `KC_CACHE=ispn` e `KC_CACHE_STACK=kubernetes`. Apos a configuracao, escalar o deployment para 3 replicas com `kubectl scale deployment/keycloak --replicas=3`. O Infinispan gerencia a replicacao de sessoes e cache entre as instancias automaticamente.

## Tuning de Performance

O connection pool do banco e configurado com `KC_DB_POOL_INITIAL_SIZE=10`, `KC_DB_POOL_MIN_SIZE=10`, `KC_DB_POOL_MAX_SIZE=50` e `KC_TRANSACTION_XA_ENABLED=false`. A configuracao de cache customizada e carregada via `KC_CACHE_CONFIG_FILE=/opt/keycloak/conf/cache-ispn.xml`.

## Estrategia de Backup

O backup automatizado e executado diariamente via cron job (`0 2 * * *`) chamando `/opt/keycloak/scripts/backup.sh`. Os backups sao enviados para S3 com `aws s3 cp /opt/keycloak/backups/ s3://carf-backups/keycloak/ --recursive`. A politica de retencao mantem backups diarios por 7 dias, semanais por 4 semanas e mensais por 12 meses.

## Monitoramento

O Prometheus coleta metricas via ServiceMonitor com selector `matchLabels: app: keycloak`, endpoint na porta HTTP e path `/metrics`. O dashboard Grafana e importado de `https://grafana.com/grafana/dashboards/10441`. Os alertas criticos incluem `KeycloakDown` (expressao `up{job="keycloak"} == 0` por 2 minutos) e `HighLoginErrors` (expressao `rate(keycloak_login_errors_total[5m]) > 10` por 5 minutos).

## Logging Estruturado

Os logs sao configurados em formato JSON com `KC_LOG_FORMAT=json` e nivel `KC_LOG_LEVEL=info`. O shipping dos logs para ELK ou CloudWatch e feito via Fluentd configurado com output para Elasticsearch.

## Gestao de Secrets

Os secrets sao armazenados no AWS Secrets Manager com entradas para `keycloak-db-password` e `keycloak-admin-password`. A integracao com o Kubernetes e feita via External Secrets aplicando `kubectl apply -f external-secrets.yaml`, que sincroniza automaticamente os valores do Secrets Manager com Kubernetes Secrets.

## Network Policies

A NetworkPolicy `keycloak-netpol` restringe o trafego de entrada ao pod Keycloak (`podSelector: app: keycloak`), permitindo apenas conexoes vindas do ingress controller (`from podSelector: app: nginx-ingress`) na porta TCP 8080.

## Disaster Recovery

O plano de disaster recovery inclui backup cruzado entre regioes com `aws s3 sync` de us-east-1 para eu-west-1. Um cluster standby na regiao secundaria e mantido pronto com `kubectl apply keycloak-deployment.yaml` no contexto eu-west-1. O failover de DNS e executado via Route53 com `change-resource-record-sets` aplicando a configuracao do arquivo `failover.json`.

## Verificacao da Configuracao

O ambiente de producao deve ter PostgreSQL RDS configurado em multi-AZ, HTTPS/TLS terminado no Load Balancer, resource limits de CPU e memoria definidos, clustering com 3 ou mais replicas ativo, connection pool otimizado, backup diario com upload para S3, Prometheus e Grafana configurados, alertas criticos ativos, logs centralizados em ELK ou CloudWatch, secrets gerenciados via Secrets Manager, network policies aplicadas e o plano de DR testado e documentado.
