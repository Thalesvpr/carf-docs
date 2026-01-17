# DEV

Overlay Kubernetes para ambiente de desenvolvimento sobrescreve configurações base através de Kustomize patches específicos para facilitar iteração rápida debugging e acesso direto aos serviços sem complexidade de produção, arquivo kustomization.yaml referencia bases ../../base como foundation aplicando replicas patch para um única réplica economizando recursos cluster local commonLabels environment igual dev identificação fácil recursos kubectl namePrefix dev- distinguindo recursos ambientes namespace carf-dev isolando deployment namespace dedicado, customizações incluem resources requests mínimos definindo cpu cinquenta millicores memory sessenta e quatro MiB permitindo startup rápido sem competição recursos imagePullPolicy Always forçando pull latest tags testando builds recentes debug logging habilitado environment variable DEBUG true aumentando verbosity logs troubleshooting NodePort services expondo portas diretamente host node acesso localhost porta alta sem ingress controller simplificando setup local persistent volumes local-path provisioner armazenando dados diretório local node reduzindo custo latência, ConfigMap dev-config sobrescreve variáveis específicas DATABASE_HOST postgres-dev apontando serviço interno namespace LOG_LEVEL debug maximizando informação logs CORS_ORIGINS asterisco permitindo requests qualquer origem facilitando desenvolvimento frontend localhost porta diferente, ambiente desenvolvimento intencionalmente não configura HPA Horizontal Pod Autoscaler mantendo replicas fixas um simplicidade nem resource limits permitindo pods consumir recursos necessários sem throttling facilitando debug memory leaks CPU spikes identificando problemas antes impactar produção.

## Arquivos Configuração

- **[kustomization.yaml](./kustomization.yaml)** - Kustomize config referencia base patches dev namePrefix namespace
- **[replica-patch.yaml](./replica-patch.yaml)** - Replicas uma economia recursos cluster local
- **[resource-patch.yaml](./resource-patch.yaml)** - Requests mínimos 50m CPU 64Mi memory startup rápido

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

