# PROD

Overlay Kubernetes para ambiente produção. kustomization.yaml (bases ../../base, replicas patch 3, commonLabels environment=prod, namespace carf-prod, images setting tags específicos v1.2.3). Customizações: resources requests/limits definidos (GEOAPI 500m/512Mi requests, 1000m/1Gi limits), HPA minReplicas 3 maxReplicas 10 targetCPU 70%, PodDisruptionBudget minAvailable 2 garantindo availability, liveness/readiness probes agressivos initialDelaySeconds 30 periodSeconds 10, RollingUpdate strategy maxUnavailable 1 maxSurge 1, PriorityClass high para scheduling. Secrets externalizados via External Secrets Operator buscando AWS Secrets Manager. Ingress com TLS cert-manager Let's Encrypt.

---

**Última atualização:** 2025-12-29
