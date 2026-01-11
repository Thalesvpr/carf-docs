# DEV

Overlay Kubernetes para ambiente de desenvolvimento sobrescreve configurações base através de Kustomize patches específicos para facilitar iteração rápida debugging e acesso direto aos serviços sem complexidade de produção. Arquivo kustomization.yaml referencia bases ../../base como foundation aplicando replicas patch para um única réplica economizando recursos cluster local, commonLabels environment igual dev para identificação fácil de recursos via kubectl, namePrefix dev- distinguindo recursos de outros ambientes, namespace carf-dev isolando deployment em namespace dedicado.

Customizações incluem resources requests mínimos definindo cpu cinquenta millicores e memory sessenta e quatro MiB permitindo startup rápido sem competição por recursos, imagePullPolicy Always forçando pull de latest tags permitindo testar builds recentes sem alterar image tag, debug logging habilitado via environment variable DEBUG igual true aumentando verbosity de logs facilitando troubleshooting, NodePort services expondo portas diretamente no host node permitindo acesso via localhost porta alta sem necessidade de ingress controller simplificando setup local, persistent volumes usando local-path provisioner armazenando dados em diretório local do node ao invés de cloud storage provider como EBS ou persistent disk reduzindo custo e latência.

ConfigMap dev-config sobrescreve variáveis específicas como DATABASE_HOST igual postgres-dev apontando para serviço interno namespace LOG_LEVEL igual debug maximizando informação logs CORS_ORIGINS asterisco permitindo requests de qualquer origem facilitando desenvolvimento frontend em localhost porta diferente. Ambiente desenvolvimento intencionalmente não configura HPA Horizontal Pod Autoscaler mantendo replicas fixas em um para simplicidade nem resource limits permitindo pods consumir recursos necessários sem throttling facilitando debug de memory leaks ou CPU spikes identificando problemas antes de impactar produção.

---

**Última atualização:** 2026-01-10
