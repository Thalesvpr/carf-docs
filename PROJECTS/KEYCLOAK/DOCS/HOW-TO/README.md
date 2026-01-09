# HOW-TO - Guias Práticos

Guias passo-a-passo para tarefas comuns de desenvolvimento e deployment.

## Arquivos

### [01-develop-themes.md](./01-develop-themes.md)
Como desenvolver temas customizados incluindo setup ambiente local com hot reload, estrutura de arquivos FreeMarker, CSS/JS bundling, testing em múltiplos browsers, e workflow dev-to-prod.

### [02-deploy-extensions.md](./02-deploy-extensions.md)
Como fazer deploy de extensões Java (SPIs) incluindo build Maven, packaging JAR, copy para /providers/, Keycloak rebuild, testing em staging, e rollout em produção com rollback strategy.

### [03-setup-dev-environment.md](./03-setup-dev-environment.md)
Configurar ambiente de desenvolvimento completo incluindo Docker Compose com Postgres, Keycloak start-dev com volume mounts, IDE setup (VS Code/IntelliJ), debugging remoto, e quick iteration loop.

### [04-build-custom-image.md](./04-build-custom-image.md)
Build de imagem Docker customizada incluindo multi-stage Dockerfile, optimization layers, tagging strategy, push para registry (ECR/ACR/Docker Hub), e scanning de vulnerabilidades.

### [05-update-keycloak-version.md](./05-update-keycloak-version.md)
Processo de atualização de versão do Keycloak incluindo changelog review, compatibility testing, theme adjustments, SPI recompilation, database migrations, e staged rollout.

### [06-configure-production.md](./06-configure-production.md)
Configuração para ambiente de produção incluindo PostgreSQL externo, HTTPS/TLS setup, resource limits (CPU/memory), clustering mode, performance tuning, backup strategy, e monitoring.

## Convenções

- **Pré-requisitos**: Listar no início de cada guia
- **Tempo estimado**: Indicar duração aproximada
- **Nível**: Iniciante / Intermediário / Avançado
- **Comandos**: Sempre com output esperado
- **Troubleshooting**: Seção ao final com erros comuns

## Referências Rápidas

- Documentação completa: `PROJECTS/KEYCLOAK/DOCS/`
- Exemplos de código: `PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/`
- Integração: `CENTRAL/INTEGRATION/KEYCLOAK/`
- Runbooks operacionais: `CENTRAL/INTEGRATION/KEYCLOAK/runbooks/`
