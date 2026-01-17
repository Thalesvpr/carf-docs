# PROD

Overlay Kubernetes para ambiente de produção implementa configurações robustas garantindo alta disponibilidade confiabilidade e segurança do sistema CARF atendendo SLA de noventa e nove ponto nove por cento uptime através de redundância autoscaling e health checks agressivos, arquivo kustomization.yaml referencia bases ../../base aplicando replicas patch para três réplicas mínimas garantindo tolerância falhas distribuição carga commonLabels environment igual prod identificando recursos produção namespace carf-prod isolando completamente dev staging images setting tags específicos v1.2.3 garantindo imutabilidade rollback confiável latest tags mutáveis, configurações resources definem requests limits precisos GEOAPI requests quinhentos millicores CPU quinhentos doze MiB memory garantindo scheduling adequado limits mil millicores um GiB prevenindo consumo excessivo impacto outros pods, HPA Horizontal Pod Autoscaler configurado minReplicas três maxReplicas dez targetCPU setenta por cento escalando automaticamente baseado carga mantendo performance picos tráfego, PodDisruptionBudget minAvailable dois garantindo sempre mínimo dois pods permanecem running durante node drains rolling updates evitando downtime completo, liveness readiness probes parâmetros agressivos initialDelaySeconds trinta periodSeconds dez timeoutSeconds cinco failureThreshold três detectando falhas rapidamente removendo pods unhealthy load balancer, RollingUpdate strategy maxUnavailable um maxSurge um permitindo atualizações graduais sem downtime novos pods criados antes terminar antigos validando saúde continuar rollout, PriorityClass high garantindo scheduling prioritário cenários resource contention produção precedência dev staging, Secrets gerenciados External Secrets Operator integrando AWS Secrets Manager Azure Key Vault buscando credenciais database Keycloak JWT automaticamente sincronizando Kubernetes Secrets sem armazenar plaintext manifests Git garantindo rotação centralizada auditoria compliance LGPD, Ingress configurado TLS cert-manager anotações provisionando automaticamente certificados Let's Encrypt renovação automática noventa dias antes expiração HTTPS válido intervenção manual, persistent volumes cloud storage classes gp3 EBS AWS premium-rw Azure Disk replication garantindo durabilidade dados database PostgreSQL snapshots automáticos diários retention trinta dias disaster recovery point-in-time restore.

## Arquivos Configuração

- **[kustomization.yaml](./kustomization.yaml)** - Kustomize config referencia base patches prod namespace images tags
- **[replica-patch.yaml](./replica-patch.yaml)** - Replicas três high availability tolerância falhas
- **[resource-patch.yaml](./resource-patch.yaml)** - Requests 500m CPU 512Mi memory limits 1000m 1Gi
- **[hpa-patch.yaml](./hpa-patch.yaml)** - HorizontalPodAutoscaler minReplicas 3 maxReplicas 10 CPU 70%
- **[pdb-patch.yaml](./pdb-patch.yaml)** - PodDisruptionBudget minAvailable 2 availability rolling updates

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

