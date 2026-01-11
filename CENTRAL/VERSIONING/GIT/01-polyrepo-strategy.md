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

Cada repositório de código deve ser clonado na pasta `SRC-CODE` correspondente dentro de `PROJECTS/` para:
- Manter organização consistente
- Permitir `.gitignore` das pastas de código
- Evitar conflitos entre repo de documentação e repos de implementação

```
carf-docs/                          # Repositório de documentação (este)
├── CENTRAL/                        # SSOT
├── PROJECTS/
│   ├── TSCORE/
│   │   ├── DOCS/                   # Docs específicas da lib TypeScript
│   │   └── SRC-CODE/               # → git clone carf-tscore aqui
│   ├── GEOAPI/
│   │   ├── DOCS/                   # Docs específicas do backend
│   │   └── SRC-CODE/               # → git clone carf-geoapi aqui
│   ├── GEOWEB/
│   │   ├── DOCS/                   # Docs específicas do frontend
│   │   └── SRC-CODE/               # → git clone carf-geoweb aqui
│   ├── REURBCAD/
│   │   ├── DOCS/                   # Docs específicas do mobile
│   │   └── SRC-CODE/               # → git clone carf-reurbcad aqui
│   ├── GEOGIS/
│   │   ├── DOCS/                   # Docs específicas do plugin
│   │   └── SRC-CODE/               # → git clone carf-geogis aqui
│   ├── WEBDOCS/
│   │   ├── DOCS/                   # Docs específicas do portal
│   │   └── SRC-CODE/               # → git clone carf-webdocs aqui
│   └── ADMIN/
│       ├── DOCS/                   # Docs específicas do console admin
│       └── SRC-CODE/               # → git clone carf-admin aqui
└── DEVELOPMENT/
```

### Comandos de Clone

**Passo 1:** Clone o repositório de documentação primeiro:

```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
```

**Passo 2:** Clone apenas os repositórios que você precisa:

```bash
# TypeScript Shared Library (Frontend/Admin Teams)
git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE

# Backend Developer (Backend Team)
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE

# Frontend Developer (Frontend Team)
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE

# Mobile Developer (Mobile Team)
git clone https://github.com/Thalesvpr/carf-reurbcad.git PROJECTS/REURBCAD/SRC-CODE

# GIS Developer (GIS Team)
git clone https://github.com/Thalesvpr/carf-geogis.git PROJECTS/GEOGIS/SRC-CODE

# Documentation Team
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE

# Admin Console (Admin Team)
git clone https://github.com/Thalesvpr/carf-admin.git PROJECTS/ADMIN/SRC-CODE
```

**Passo 3:** Acesse o README específico de cada projeto para instruções de build/run/test:

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

**Backend Developer:**
```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
# Trabalha apenas no backend, ignora frontend/mobile/plugin
```

**Frontend Developer:**
```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE
# Trabalha em frontend + biblioteca compartilhada, ignora backend/mobile/plugin
```

**Full Stack Developer:**
```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE
# Trabalha em backend e frontend, ignora mobile/plugin
```

**Tech Lead / Arquiteto:**
```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
# Clona todos os repositórios
git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE
git clone https://github.com/Thalesvpr/carf-reurbcad.git PROJECTS/REURBCAD/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geogis.git PROJECTS/GEOGIS/SRC-CODE
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
git clone https://github.com/Thalesvpr/carf-admin.git PROJECTS/ADMIN/SRC-CODE
```

## Workflow de Trabalho

### Trabalhando em um Repositório Específico

```bash
# Entre na pasta SRC-CODE do projeto
cd PROJECTS/GEOAPI/SRC-CODE

# Trabalhe normalmente com Git
git checkout -b feature/nova-funcionalidade
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade

# Volte para a raiz da documentação
cd ../../..
```

### Trabalhando no @carf/tscore (Biblioteca Compartilhada)

Workflow específico para desenvolver na biblioteca compartilhada:

```bash
# Clonar tscore se ainda não tiver
git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE
cd PROJECTS/TSCORE/SRC-CODE

# Instalar dependências
bun install

# Criar branch para feature
git checkout -b feature/add-crea-validation

# Desenvolver (ex: adicionar novo value object CREA)
# Editar src/validations/crea.ts
# Adicionar testes src/validations/__tests__/crea.test.ts

# Rodar testes
bun test

# Build para verificar
bun run build

# Testar localmente em projeto consumidor (GEOWEB)
npm link
cd ../../../GEOWEB/SRC-CODE
npm link @carf/tscore
# Testar mudanças no GEOWEB
# Desfazer link quando terminar: npm unlink @carf/tscore && bun install

# Voltar ao tscore para commit
cd ../../../TSCORE/SRC-CODE
git add .
git commit -m "feat: add CREA value object validation"
git push origin feature/add-crea-validation

# Criar PR no GitHub
gh pr create --title "feat: Add CREA validation" --body "..."

# Após merge na main, publicar nova versão (CI/CD automático)
# Ou manualmente:
npm version minor  # Incrementa versão (0.1.0 → 0.2.0)
git push --follow-tags  # Dispara CI/CD que publica no GitHub Packages
```

**Importante:**
- Sempre rodar `bun test` antes de commitar
- Usar `npm link` para testar localmente antes de publicar
- Seguir [Conventional Commits](./03-commit-conventions.md)
- Atualizar [CHANGELOG.md](../../../PROJECTS/LIB/TS/TSCORE/SRC-CODE/CHANGELOG.md) antes de publicar
- Breaking changes requerem MAJOR version bump

### Atualizando Documentação

```bash
# Na raiz do carf-docs
git checkout -b docs/atualiza-requisito
# Edite arquivos em CENTRAL/, PROJECTS/, etc.
git add .
git commit -m "docs: atualiza requisito RF-001"
git push origin docs/atualiza-requisito
```

### Sincronizando Mudanças

```bash
# Atualizar documentação
git pull origin main

# Atualizar cada repositório de código
cd PROJECTS/GEOAPI/SRC-CODE && git pull origin main && cd ../../..
cd PROJECTS/GEOWEB/SRC-CODE && git pull origin main && cd ../../..
cd PROJECTS/TSCORE/SRC-CODE && git pull origin main && cd ../../..
# Repita para outros repositórios conforme necessário
```

### Atualizando @carf/tscore em Projetos Consumidores

Quando nova versão do tscore é publicada:

```bash
# GEOWEB
cd PROJECTS/GEOWEB/SRC-CODE
bun update @carf/tscore
# Verificar CHANGELOG do tscore para breaking changes
cat node_modules/@carf/tscore/CHANGELOG.md
# Testar aplicação
bun dev
# Commit se houver mudanças necessárias
git add package.json bun.lockb
git commit -m "chore: update @carf/tscore to v0.2.0"

# REURBCAD
cd ../../../REURBCAD/SRC-CODE
bun update @carf/tscore
# Testar app mobile
bun android
# Commit
git add package.json bun.lockb
git commit -m "chore: update @carf/tscore to v0.2.0"

# ADMIN
cd ../../../ADMIN/SRC-CODE
bun update @carf/tscore
# Testar console
bun dev
# Commit
git add package.json bun.lockb
git commit -m "chore: update @carf/tscore to v0.2.0"

# WEBDOCS
cd ../../../WEBDOCS/SRC-CODE
bun update @carf/tscore
# Testar portal
bun dev
# Commit
git add package.json bun.lockb
git commit -m "chore: update @carf/tscore to v0.2.0"
```

**Breaking Changes:**
Se tscore teve MAJOR version bump (ex: 1.0.0 → 2.0.0):
1. Ler CHANGELOG completo
2. Seguir migration guide
3. Atualizar código consumidor
4. Rodar todos os testes
5. Testar manualmente
6. Criar PR coordenado em cada projeto

## Compatibilidade entre Repositórios

Consulte o arquivo `CENTRAL/VERSIONING/GIT/06-release-coordination.md` para:
- Matriz de compatibilidade de versões
- Processo de coordenação de releases
- Estratégia de versionamento semântico
- Procedimentos de hotfix coordenados

---

**Última atualização:** 2026-01-08
