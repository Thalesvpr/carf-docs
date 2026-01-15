# Polyrepo Strategy

Estratégia polyrepo do CARF com **8 repositórios Git independentes** permitindo deploy/versionamento/ownership separados por equipe especializada.

## Repositórios

| Repositório | Descrição | Ownership | URL |
|-------------|-----------|-----------|-----|
| **carf-docs** | Documentação central (SSOT) | Tech Writers | https://github.com/Thalesvpr/carf-docs |
| **carf-tscore** | Biblioteca TypeScript compartilhada | Frontend Team | https://github.com/Thalesvpr/carf-tscore |
| **carf-geoapi** | Backend .NET 9 | Backend Team | https://github.com/Thalesvpr/carf-geoapi |
| **carf-geoweb** | Frontend React | Frontend Team | https://github.com/Thalesvpr/carf-geoweb |
| **carf-reurbcad** | Mobile React Native | Mobile Team | https://github.com/Thalesvpr/carf-reurbcad |
| **carf-geogis** | Plugin QGIS Python | GIS Team | https://github.com/Thalesvpr/carf-geogis |
| **carf-webdocs** | Portal VitePress | Docs Team | https://github.com/Thalesvpr/carf-webdocs |
| **carf-admin** | Console administrativo Next.js | Admin Team | https://github.com/Thalesvpr/carf-admin |

## Vantagens

- **Deploys independentes:** Hotfix no backend sem rebuild do frontend
- **Ownership claro:** Cada equipe responsável por seu repositório
- **CI/CD otimizado:** Pipeline roda apenas no repo modificado
- **Onboarding focado:** Dev frontend clona apenas geoweb, backend apenas geoapi
- **Controle de acesso:** Permissões granulares por repositório no GitHub
- **Histórico limpo:** Commits organizados por contexto de negócio

## Desvantagens e Mitigações

| Desvantagem | Mitigação |
|-------------|-----------|
| Coordenação de releases complexa | Usar `compatibility-matrix.md` versionando combinações testadas |
| Code sharing via packages | @carf/tscore NPM package para TypeScript shared code |
| Dependency hell entre repos | Versionamento semântico estrito + renovate/dependabot |
| Mudanças cross-repo difíceis | PRs coordenados + feature flags para rollout gradual |

Se o projeto crescer muito, considerar migração para **monorepo** com tooling (Nx/Turborepo).

## Setup Local

### Estrutura de Diretórios

Cada repositório de código deve ser clonado na pasta SRC-CODE correspondente dentro de PROJECTS/ mantendo organização consistente permitindo gitignore das pastas de código e evitando conflitos entre repo de documentação e repos de implementação.

Estrutura organizada com repositório carf-docs na raiz contendo diretório CENTRAL como SSOT seguido por PROJECTS/ contendo sete projetos sendo TSCORE com subdiretório DOCS para documentação específica da lib TypeScript e SRC-CODE para clonar carf-tscore, GEOAPI com DOCS para documentação específica do backend e SRC-CODE para clonar carf-geoapi, GEOWEB com DOCS para documentação específica do frontend e SRC-CODE para clonar carf-geoweb, REURBCAD com DOCS para documentação específica do mobile e SRC-CODE para clonar carf-reurbcad, GEOGIS com DOCS para documentação específica do plugin e SRC-CODE para clonar carf-geogis, WEBDOCS com DOCS para documentação específica do portal e SRC-CODE para clonar carf-webdocs, e ADMIN com DOCS para documentação específica do console admin e SRC-CODE para clonar carf-admin, finalizando com diretório DEVELOPMENT/ na raiz.

### Comandos de Clone

Primeiro passo executar git clone do repositório https://github.com/Thalesvpr/carf-docs.git seguido por cd carf-docs para entrar no diretório. Segundo passo clonar apenas os repositórios necessários conforme perfil do desenvolvedor sendo TypeScript Shared Library para Frontend/Admin Teams executando git clone https://github.com/Thalesvpr/carf-tscore.git especificando target directory PROJECTS/TSCORE/SRC-CODE, Backend Developer para Backend Team executando git clone https://github.com/Thalesvpr/carf-geoapi.git para PROJECTS/GEOAPI/SRC-CODE, Frontend Developer para Frontend Team executando git clone https://github.com/Thalesvpr/carf-geoweb.git para PROJECTS/GEOWEB/SRC-CODE, Mobile Developer para Mobile Team executando git clone https://github.com/Thalesvpr/carf-reurbcad.git para PROJECTS/REURBCAD/SRC-CODE, GIS Developer para GIS Team executando git clone https://github.com/Thalesvpr/carf-geogis.git para PROJECTS/GEOGIS/SRC-CODE, Documentation Team executando git clone https://github.com/Thalesvpr/carf-webdocs.git para PROJECTS/WEBDOCS/SRC-CODE, e Admin Console para Admin Team executando git clone https://github.com/Thalesvpr/carf-admin.git para PROJECTS/ADMIN/SRC-CODE.

Terceiro passo acessar o README específico de cada projeto para instruções de build/run/test:

- TypeScript Library: (caminho de implementação)
- Backend: (caminho de implementação)
- Frontend: (caminho de implementação)
- Mobile: (caminho de implementação)
- QGIS Plugin: (caminho de implementação)
- Docs Portal: (caminho de implementação)
- Admin Console: (caminho de implementação)

### .gitignore

As pastas `SRC-CODE/` estão no `.gitignore` do repositório `carf-docs`, permitindo que:
- Cada desenvolvedor clone apenas os repositórios necessários
- Não haja conflitos entre repositórios aninhados
- Histórico Git da documentação permaneça limpo

### Exemplos de Uso por Perfil

Backend Developer executa git clone do repositório carf-docs seguido por cd carf-docs e clona carf-geoapi para PROJECTS/GEOAPI/SRC-CODE trabalhando apenas no backend ignorando frontend mobile e plugin. Frontend Developer executa git clone do carf-docs seguido por cd carf-docs clonando carf-tscore para PROJECTS/TSCORE/SRC-CODE e carf-geoweb para PROJECTS/GEOWEB/SRC-CODE trabalhando em frontend mais biblioteca compartilhada ignorando backend mobile e plugin. Full Stack Developer executa git clone do carf-docs seguido por cd carf-docs clonando carf-geoapi para PROJECTS/GEOAPI/SRC-CODE e carf-geoweb para PROJECTS/GEOWEB/SRC-CODE trabalhando em backend e frontend ignorando mobile e plugin. Tech Lead ou Arquiteto executa git clone do carf-docs seguido por cd carf-docs clonando todos os repositórios sendo carf-tscore para PROJECTS/TSCORE/SRC-CODE, carf-geoapi para PROJECTS/GEOAPI/SRC-CODE, carf-geoweb para PROJECTS/GEOWEB/SRC-CODE, carf-reurbcad para PROJECTS/REURBCAD/SRC-CODE, carf-geogis para PROJECTS/GEOGIS/SRC-CODE, carf-webdocs para PROJECTS/WEBDOCS/SRC-CODE, e carf-admin para PROJECTS/ADMIN/SRC-CODE permitindo visão completa de todos projetos.

## Workflow de Trabalho

### Trabalhando em um Repositório Específico

Para trabalhar em repositório específico entrar na pasta SRC-CODE do projeto usando cd PROJECTS/GEOAPI/SRC-CODE seguido por operações Git normais criando branch com git checkout menos b feature/nova-funcionalidade adicionando mudanças com git add ponto fazendo commit com git commit menos m "feat: adiciona nova funcionalidade" enviando para remote com git push origin feature/nova-funcionalidade e voltando para raiz da documentação com cd ponto ponto ponto barra ponto ponto ponto barra ponto ponto ponto.

### Trabalhando no @carf/tscore (Biblioteca Compartilhada)

Workflow específico para desenvolver na biblioteca compartilhada inicia clonando tscore se ainda não tiver executando git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE seguido por cd PROJECTS/TSCORE/SRC-CODE e instalando dependências com bun install, criar branch para feature usando git checkout menos b feature/add-crea-validation desenvolvendo exemplo adicionando novo value object CREA editando src/validations/crea.ts e adicionando testes em src/validations/__tests__/crea.test.ts, rodando testes com bun test e build para verificar com bun run build.

Testar localmente em projeto consumidor GEOWEB executando npm link na pasta tscore seguido por cd ../../../GEOWEB/SRC-CODE e npm link @carf/tscore testando mudanças no GEOWEB desfazendo link quando terminar com npm unlink @carf/tscore && bun install, voltar ao tscore para commit usando cd ../../../TSCORE/SRC-CODE seguido por git add ponto git commit menos m "feat: add CREA value object validation" e git push origin feature/add-crea-validation, criar PR no GitHub executando gh pr create menos menos title "feat: Add CREA validation" menos menos body com descrição.

Após merge na main publicar nova versão usando CI/CD automático ou manualmente executando npm version minor incrementando versão de zero ponto um ponto zero para zero ponto dois ponto zero seguido por git push menos menos follow-tags disparando CI/CD que publica no GitHub Packages. Importante sempre rodar bun test antes de commitar usar npm link para testar localmente antes de publicar seguir Conventional Commits atualizar CHANGELOG.md antes de publicar e breaking changes requerem MAJOR version bump.

### Atualizando Documentação

Para atualizar documentação na raiz do carf-docs executar git checkout menos b docs/atualiza-requisito editando arquivos em CENTRAL/ PROJECTS/ ou outros diretórios seguido por git add ponto git commit menos m "docs: atualiza requisito RF-001" e git push origin docs/atualiza-requisito.

### Sincronizando Mudanças

Sincronizar mudanças executando git pull origin main para atualizar documentação seguido por atualização de cada repositório de código navegando para PROJECTS/GEOAPI/SRC-CODE executando git pull origin main e retornando com cd ../../.. repetindo processo para PROJECTS/GEOWEB/SRC-CODE e PROJECTS/TSCORE/SRC-CODE e outros repositórios conforme necessário mantendo todos projetos atualizados com branches main remotas.

### Atualizando @carf/tscore em Projetos Consumidores

Quando nova versão do tscore é publicada atualizar GEOWEB navegando para PROJECTS/GEOWEB/SRC-CODE executando bun update @carf/tscore verificando CHANGELOG do tscore para breaking changes com cat node_modules/@carf/tscore/CHANGELOG.md testando aplicação com bun dev e commitando se houver mudanças necessárias executando git add package.json bun.lockb seguido por git commit menos m "chore: update @carf/tscore to v0.2.0", atualizar REURBCAD navegando para ../../../REURBCAD/SRC-CODE executando bun update @carf/tscore testando app mobile com bun android e commitando com git add package.json bun.lockb git commit menos m "chore: update @carf/tscore to v0.2.0", atualizar ADMIN navegando para ../../../ADMIN/SRC-CODE executando bun update @carf/tscore testando console com bun dev e commitando com git add package.json bun.lockb git commit menos m "chore: update @carf/tscore to v0.2.0", e atualizar WEBDOCS navegando para ../../../WEBDOCS/SRC-CODE executando bun update @carf/tscore testando portal com bun dev e commitando com git add package.json bun.lockb git commit menos m "chore: update @carf/tscore to v0.2.0".

Breaking Changes se tscore teve MAJOR version bump exemplo um ponto zero ponto zero para dois ponto zero ponto zero seguir processo ler CHANGELOG completo seguir migration guide atualizar código consumidor rodar todos os testes testar manualmente e criar PR coordenado em cada projeto garantindo compatibilidade cross-repo.

## Compatibilidade entre Repositórios

Para matriz de compatibilidade de versões, processo de coordenação de releases, estratégia de versionamento semântico e procedimentos de hotfix coordenados, consulte 06-release-coordination.

---

**Última atualização:** 2026-01-08
