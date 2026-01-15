# ADR-020: Escolha do Docker + Kubernetes para Orquestração Backend

Decisão arquitetural escolhendo Docker para containerização e Kubernetes para orquestração do backend GEOAPI justificada por isolamento completo de dependencies eliminando conflicts de versões e "works on my machine" problems garantindo ambiente idêntico dev/staging/prod, immutable infrastructure permitindo deploys confiáveis e rollbacks instantâneos via image tags, resource limits (CPU/memory) prevenindo noisy neighbor problems em multi-tenant deployments, horizontal scaling automático via HPA (Horizontal Pod Autoscaler) escalando pods baseado em CPU/memória handling picos de tráfego sem intervenção manual, self-healing com automatic restart de pods unhealthy mantendo availability alta, rolling updates zero-downtime deployando novas versões gradualmente verificando health antes de substituir pods antigos, service discovery automático via Kubernetes DNS eliminando hardcoded IPs, secrets management com encryption at rest para database credentials API keys, e portabilidade entre cloud providers evitando vendor lock-in permitindo migration AWS→Azure→GCP mantendo mesma infra config.

Docker multi-stage builds otimizam image size separando build dependencies de runtime (~200MB final vs ~1GB sem optimization), Kubernetes StatefulSet gerencia PostgreSQL com persistent volumes garantindo durabilidade de dados, e Ingress controller (nginx) gerencia routing SSL termination.

Alternativas consideradas incluem Docker Swarm (rejeitado por features limitadas comparado a Kubernetes e declínio de adoção), Nomad (rejeitado por ecosystem menor), ECS Fargate (rejeitado por vendor lock-in AWS), Cloud Run (rejeitado por limitações de stateful workloads), VMs tradicionais (rejeitado por overhead operacional e deployment lento), e bare metal (rejeitado por ausência de orchestration automation).

Consequências positivas incluem deployment confiável, scaling automático, self-healing, portabilidade cloud, e ecosistema rico. Consequências negativas incluem curva aprendizado Kubernetes, overhead operacional gerenciando cluster, e custo de control plane.

Configuração utiliza Docker 24+ com multi-stage builds, Kubernetes 1.28+ com HPA escalando 2-10 pods baseado em CPU 70%, persistent volumes para PostgreSQL, ConfigMaps para env variables, Secrets para credentials, e Helm charts versionando manifests.

Status aprovado e implementado desde 2024-Q3.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + DevOps
**Última revisão:** 2025-01-10
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
