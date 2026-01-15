# Orchestration

Orquestração Kubernetes (cloud) ou Docker Swarm (on-premises) garantindo alta disponibilidade e escalabilidade conforme ADR-020. Deployments com ReplicaSets configurados (GEOAPI min 3 replicas, GEOWEB min 2 replicas) distribuídos cross-zone evitando single point of failure, rollingUpdate strategy com maxSurge 1 maxUnavailable 0 garantindo zero-downtime, readinessProbe HTTP GET /health/ready bloqueando tráfego até app inicializada, e livenessProbe detectando deadlocks reiniciando pods automaticamente. HorizontalPodAutoscaler escalando baseado em métricas (CPU >70%, memória >80%, custom metrics como fila RabbitMQ depth >1000) com cooldown 5min evitando flapping, scale-up agressivo (doubling replicas), e scale-down conservador (reduzindo 1 por vez). Services LoadBalancer ou NodePort expondo pods com sessionAffinity ClientIP quando stateful necessário, Ingress NGINX configurado com TLS termination, rate limiting per-tenant (100 req/min padrão, 1000 req/min premium), e path-based routing (/api → GEOAPI, / → GEOWEB). ConfigMaps montando configs não-sensíveis (feature flags, URLs públicas), Secrets montando credenciais (DB passwords, JWT secrets) criptografados at-rest via KMS, e volumes PersistentVolumeClaim para PostgreSQL data (SSD, 100GB, backup automático).

## Projetos Orquestrados

Kubernetes orquestra deployments de com HPA (Horizontal Pod Autoscaler) escalando pods baseado em CPU/memória para lidar com picos de uso em horários comerciais scaling 2→10 replicas automaticamente, em cluster mode com shared cache Redis para sessions multi-realm conforme ADR-005 permitindo load balancing stateless entre replicas, e PostgreSQL em StatefulSet com persistent volumes garantindo durabilidade de dados geográficos PostGIS conforme ADR-002, enquanto e usam Vercel (ADR-013) serverless auto-scaling sem necessidade de Kubernetes.

---

**Última atualização:** 2026-01-10
**Status do arquivo**: Pronto
