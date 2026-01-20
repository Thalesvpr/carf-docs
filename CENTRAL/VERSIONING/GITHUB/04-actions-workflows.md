# Workflows de Actions

Pipelines CI/CD implementados com GitHub Actions para automação de build, test, lint e deploy dos repositórios CARF. Cada repositório possui workflows específicos para sua stack mantendo padrões consistentes de qualidade.

## Estrutura de Workflows

Workflows ficam em .github/workflows/ de cada repositório. O arquivo ci.yml executa em pull requests para validar mudanças. O arquivo cd.yml executa em push para main para deploy automatizado. Workflows adicionais como release.yml e security.yml complementam a automação.

## Workflow CI Padrão

O workflow de CI executa em eventos pull_request para branches main e develop. Jobs incluem checkout do código, setup do ambiente (Node.js, .NET, Python conforme stack), instalação de dependências, execução de linter, execução de testes unitários, build do projeto e upload de artefatos quando aplicável.

## Workflows por Repositório

| Repositório | CI Jobs | CD Jobs | Ambiente |
|-------------|---------|---------|----------|
| carf-geoapi | build, test, lint | deploy-staging, deploy-prod | Azure Container Apps |
| carf-geoweb | build, test, lint, type-check | deploy-staging, deploy-prod | Vercel |
| carf-reurbcad | build, test, lint | build-apk, build-ipa | Expo EAS |
| carf-geogis | lint, test | package-plugin | QGIS Plugin Repository |
| carf-webdocs | build, lint | deploy-docs | GitHub Pages |
| carf-keycloak | build-image, test | push-registry, deploy | Docker Registry |

## Secrets e Variáveis

Secrets são configurados em Settings > Secrets and variables > Actions de cada repositório. Secrets comuns incluem AZURE_CREDENTIALS para deploy Azure, VERCEL_TOKEN para deploy Vercel, DOCKER_USERNAME e DOCKER_PASSWORD para registry, NPM_TOKEN para publicação de packages. Variáveis de ambiente não sensíveis ficam em vars como ENVIRONMENT_NAME e API_URL.

## Reutilização de Workflows

Workflows compartilhados podem ser definidos em repositório central e referenciados via uses: owner/repo/.github/workflows/workflow.yml@main. Isso permite padronizar jobs comuns como lint e security scan entre repositórios sem duplicação de código.

## Monitoramento

GitHub Actions Dashboard mostra status de execuções recentes. Falhas em workflows de CI bloqueiam merge do PR. Falhas em CD disparam notificações para o time responsável. Métricas de tempo de execução e taxa de sucesso são revisadas mensalmente para otimização.

## Cache e Performance

Workflows devem usar actions/cache para dependências (node_modules, NuGet packages, pip cache) reduzindo tempo de execução. Setup actions como actions/setup-node e actions/setup-dotnet oferecem cache integrado. Jobs independentes devem executar em paralelo usando matrix strategy quando aplicável.

---

**Status:** Review
**Atualizado:** 2026-01-20
**Descrição:**
