# DEV

Overlay Kubernetes para ambiente desenvolvimento. kustomization.yaml (bases ../../base, replicas patch 1, commonLabels environment=dev, namePrefix dev-, namespace carf-dev). Customizações: resources requests mínimos (cpu 50m, memory 64Mi), imagePullPolicy Always para testar latest tags, debug logging enabled via env DEBUG=true, NodePort services exposing para acesso fácil sem ingress, persistent volumes usando local-path provisioner ao invés cloud. ConfigMap dev-config com DATABASE_HOST=postgres-dev, LOG_LEVEL=debug. Não tem HPA, não tem resource limits para facilitar debug.

---

**Última atualização:** 2025-12-29
