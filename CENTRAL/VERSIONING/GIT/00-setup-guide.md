# Guia de Setup - CARF Polyrepo

Guia passo a passo para configurar o ambiente de desenvolvimento do CARF seguindo a arquitetura polyrepo.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Git** (versão 2.30+): https://git-scm.com/downloads
- **GitHub CLI** (opcional, mas recomendado): https://cli.github.com/
- Ferramentas específicas por projeto:
  - Backend: .NET 9 SDK
  - Frontend: Node.js 20+ (ou Bun runtime)
  - Mobile: Node.js 20+, React Native CLI
  - QGIS Plugin: Python 3.x, QGIS 3.x
  - Docs Portal: Node.js 20+

## Setup Rápido

### Para Desenvolvedores (Apenas o que você precisa)

**1. Clone o repositório de documentação:** Executar git clone do repositório carf-docs do GitHub seguido por cd carf-docs para entrar no diretório.

**2. Clone apenas seu projeto:** Backend developers clonam carf-geoapi para PROJECTS/GEOAPI/SRC-CODE, frontend developers clonam carf-geoweb para PROJECTS/GEOWEB/SRC-CODE, mobile developers clonam carf-reurbcad para PROJECTS/REURBCAD/SRC-CODE, GIS developers clonam carf-geogis para PROJECTS/GEOGIS/SRC-CODE, documentation team clona carf-webdocs para PROJECTS/WEBDOCS/SRC-CODE usando git clone com target directory apropriado.

**3. Siga as instruções do projeto:** Acesse o README do projeto que você clonou em PROJECTS/*/SRC-CODE/README.md para instruções específicas de setup build e desenvolvimento.

## Setup Completo

### Para Tech Leads, Arquitetos e DevOps

**1. Clone o repositório de documentação:** Executar git clone do repositório carf-docs do GitHub seguido por cd carf-docs para entrar no diretório.

**2. Clone todos os repositórios:** Executar git clone para cada projeto especificando target directory sendo carf-geoapi para PROJECTS/GEOAPI/SRC-CODE, carf-geoweb para PROJECTS/GEOWEB/SRC-CODE, carf-reurbcad para PROJECTS/REURBCAD/SRC-CODE, carf-geogis para PROJECTS/GEOGIS/SRC-CODE, e carf-webdocs para PROJECTS/WEBDOCS/SRC-CODE completando setup de todos cinco repositórios independentes.

**3. Verificar estrutura:** Executar tree comando com flags -L 3 -d PROJECTS/ para visualizar estrutura de diretórios esperada mostrando cada projeto com subdiretórios DOCS versionado em carf-docs e SRC-CODE contendo repositório Git independente ignorado por gitignore garantindo separação correta entre documentação e código-fonte.

## Estrutura de Diretórios Explicada

Repositório carf-docs organizado com gitignore configurado ignorando pastas SRC-CODE, README.md com visão geral do projeto, diretório CENTRAL como Single Source of Truth contendo REQUIREMENTS com duzentos e vinte e dois requisitos funcionais, ARCHITECTURE com ADRs deployment patterns, API com contratos REST, TECHNICAL com modelo de domínio, GIT com estratégia polyrepo, INTEGRATION com protocolos de integração, e SECURITY com políticas de segurança, seguido por diretório PROJECTS contendo projetos individuais GEOAPI GEOWEB REURBCAD GEOGIS e WEBDOCS cada um com subdiretório DOCS versionado no carf-docs e subdiretório SRC-CODE com repositório Git independente gitignored, finalizando com DEVELOPMENT contendo INFRASTRUCTURE e OPERATIONS para infraestrutura e operações do sistema.

## Como o .gitignore Funciona

Arquivo gitignore na raiz do carf-docs contém entradas para PROJECTS/GEOAPI/SRC-CODE/, PROJECTS/GEOWEB/SRC-CODE/, PROJECTS/REURBCAD/SRC-CODE/, PROJECTS/GEOGIS/SRC-CODE/, e PROJECTS/WEBDOCS/SRC-CODE/ garantindo que pastas DOCS são versionadas no carf-docs enquanto pastas SRC-CODE são ignoradas permitindo cada SRC-CODE ser repositório Git independente sem conflitos possibilitando trabalhar em múltiplos repos simultaneamente sem interferência.

## Workflow de Trabalho

### Cenário 1: Atualizar Documentação

Na raiz do carf-docs criar branch docs/atualiza-rf-001 usando git checkout menos b, editar arquivos em CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/, fazer commit com mensagem descritiva usando git add ponto git commit menos m mensagem, push origin branch, e criar PR no GitHub usando gh pr create especificando título e body descrevendo mudanças na documentação.

### Cenário 2: Desenvolver Feature no Backend

Entrar no repositório backend em PROJECTS/GEOAPI/SRC-CODE, criar branch feature/nova-api-endpoint usando git checkout menos b, desenvolver editando arquivos como Controllers em src/Gateway/Controllers/, fazer commit com mensagem feat adicionando descrição do endpoint, push origin branch, e criar PR no carf-geoapi especificando RF implementado no body do PR.

### Cenário 3: Mudança Cross-Repo (Backend + Frontend)

Implementar backend primeiro criando branch feature/new-filter-api em PROJECTS/GEOAPI/SRC-CODE desenvolvendo API commitando com mensagem feat, seguido por frontend criando branch feature/new-filter-ui em PROJECTS/GEOWEB/SRC-CODE implementando UI commitando com mensagem feat, finalmente criar PRs coordenados usando gh pr create onde PR do frontend referencia PR do backend no body indicando dependência entre mudanças cross-repo garantindo ordem correta de merge.

### Cenário 4: Atualizar Todos os Repositórios

Atualizar documentação executando git pull origin main na raiz do carf-docs seguido por loop para cada projeto em GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS verificando se diretório PROJECTS/projeto/SRC-CODE/.git existe navegando para diretório executando git pull origin main retornando para raiz repetindo para próximo projeto até atualizar todos repositórios de código, processo pode ser automatizado criando script .scripts/update-all-repos.sh para reutilização.

## Verificação de Saúde

### Verificar Estado de Todos os Repositórios

Criar script .scripts/check-repos-status.sh executando git status menos sb para carf-docs seguido por loop para cada projeto executando git status menos sb em PROJECTS/projeto/SRC-CODE mostrando branch atual e estado de working directory de cada repositório permitindo visualização rápida de estado de todos repos simultaneamente, tornar script executável com chmod mais x e executar para verificação completa.

### Verificar Branches

Executar loop para cada projeto navegando para PROJECTS/projeto/SRC-CODE executando git branch menos menos show-current exibindo branch atual de cada repositório permitindo confirmar que todos estão em branches corretas antes de começar desenvolvimento ou após trocar contexto entre features.

## Troubleshooting

**Erro fatal not a git repository:** Verificar se está na pasta correta usando pwd, se em PROJECTS/GEOAPI/SRC-CODE mas vazia clonar repositório carf-geoapi para esse local usando git clone com target directory especificado.

**Erro destination path already exists:** Remover pasta existente usando rm menos rf PROJECTS/projeto/SRC-CODE com cuidado seguido por git clone novamente para target directory limpo.

**Conflito Your branch and origin/main have diverged:** Opção 1 usar git pull menos menos rebase origin main recomendado, Opção 2 usar git pull origin main para merge, Opção 3 usar git fetch origin seguido por git reset menos menos hard origin/main perdendo mudanças locais apenas se necessário.

**Esqueci de clonar na pasta SRC-CODE correta:** Mover repositório clonado para local correto usando mv carf-projeto PROJECTS/PROJETO/SRC-CODE ou remover pasta errada e clonar novamente para target directory correto evitando confusão de estrutura.

## Próximos Passos

1. ✅ Setup concluído
2. 📖 Ler documentação específica do projeto em PROJECTS/*/DOCS/README.md
3. 🔧 Configurar ambiente de desenvolvimento (Docker, variáveis de ambiente, etc.)
4. 🏃 Executar projeto localmente
5. 🧪 Rodar testes
6. 💻 Começar a desenvolver!

## Referências

Consulte 01-polyrepo-strategy para justificativa da arquitetura, 02-branching-strategy para workflow de branches, 03-commit-conventions para formato de commits, 04-pr-guidelines para processo de PR, e 06-release-coordination para coordenação de releases.

---

**Status:** Review
**Atualizado:** 2026-01-19
**Descrição:** 
