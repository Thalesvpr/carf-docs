# Plano de Reorganização - CARF

## Problema Atual

Os repositórios Git estão diretamente dentro das pastas `SRC-CODE`, quando deveriam estar dentro de subpastas nomeadas.

### Estrutura Atual (Errada)
```
PROJECTS/
├── GEOAPI/
│   ├── DOCS/
│   └── SRC-CODE/          ← .git está aqui diretamente
│       ├── .git/
│       ├── src/
│       └── tests/
│
├── GEOWEB/
│   ├── DOCS/
│   └── SRC-CODE/          ← .git está aqui diretamente
│       ├── .git/
│       ├── src/
│       └── public/
```

### Estrutura Correta (Proposta)
```
PROJECTS/
├── GEOAPI/
│   ├── DOCS/
│   │   ├── ARCHITECTURE/
│   │   ├── CONCEPTS/
│   │   ├── HOW-TO/
│   │   └── LAYERS/
│   └── SRC-CODE/
│       └── carf-geoapi/   ← repo dentro desta pasta
│           ├── .git/
│           ├── src/
│           ├── tests/
│           ├── README.md
│           └── .gitignore
│
├── GEOWEB/
│   ├── DOCS/
│   │   ├── ARCHITECTURE/
│   │   ├── CONCEPTS/
│   │   ├── HOW-TO/
│   │   └── LAYERS/
│   └── SRC-CODE/
│       └── carf-geoweb/   ← repo dentro desta pasta
│           ├── .git/
│           ├── src/
│           ├── public/
│           ├── README.md
│           └── .gitignore
│
├── REURBCAD/
│   ├── DOCS/
│   │   ├── ARCHITECTURE/
│   │   ├── CONCEPTS/
│   │   ├── HOW-TO/
│   │   └── LAYERS/
│   └── SRC-CODE/
│       └── carf-reurbcad/ ← repo dentro desta pasta
│           ├── .git/
│           ├── android/
│           ├── ios/
│           ├── src/
│           └── README.md
│
├── GEOGIS/
│   ├── DOCS/
│   └── SRC-CODE/
│       └── carf-geogis/   ← repo dentro desta pasta
│           ├── .git/
│           ├── ui/
│           ├── utils/
│           └── README.md
│
├── WEBDOCS/
│   ├── DOCS/
│   └── SRC-CODE/
│       └── carf-webdocs/  ← repo dentro desta pasta
│           ├── .git/
│           ├── docs/
│           └── .vitepress/
│
├── ADMIN/
│   ├── DOCS/
│   └── SRC-CODE/
│       └── carf-admin/    ← repo dentro desta pasta
│           ├── .git/
│           ├── src/
│           └── README.md
│
└── TSCORE/
    ├── DOCS/
    └── SRC-CODE/
        └── carf-tscore/   ← repo dentro desta pasta
            ├── .git/
            ├── src/
            ├── dist/
            ├── package.json
            └── README.md
```

---

## Comandos para Reorganização

### 1. GEOAPI (.NET 9 Backend)
```bash
cd /c/DEV/CARF/PROJECTS/GEOAPI/SRC-CODE
mkdir carf-geoapi
mv .git .gitignore README.md src tests carf-geoapi/
```

### 2. GEOWEB (React Web App)
```bash
cd /c/DEV/CARF/PROJECTS/GEOWEB/SRC-CODE
mkdir carf-geoweb
mv .git .gitignore README.md src public carf-geoweb/
```

### 3. REURBCAD (React Native Mobile)
```bash
cd /c/DEV/CARF/PROJECTS/REURBCAD/SRC-CODE
mkdir carf-reurbcad
mv .git .gitignore README.md src android ios carf-reurbcad/
```

### 4. GEOGIS (Python QGIS Plugin)
```bash
cd /c/DEV/CARF/PROJECTS/GEOGIS/SRC-CODE
mkdir carf-geogis
mv .git .gitignore README.md ui utils resources tests carf-geogis/
```

### 5. WEBDOCS (VitePress Docs)
```bash
cd /c/DEV/CARF/PROJECTS/WEBDOCS/SRC-CODE
mkdir carf-webdocs
mv .git .gitignore README.md docs .vitepress package.json carf-webdocs/
```

### 6. ADMIN (Next.js Admin Console)
```bash
cd /c/DEV/CARF/PROJECTS/ADMIN/SRC-CODE
mkdir carf-admin
# Verificar o que existe primeiro e mover
```

### 7. TSCORE (TypeScript Shared Library)
```bash
cd /c/DEV/CARF/PROJECTS/TSCORE/SRC-CODE
mkdir carf-tscore
mv .git .gitignore .npmrc README.md CHANGELOG.md src dist package.json bun.lock carf-tscore/
```

---

## Benefícios da Nova Estrutura

### 1. Clareza
- Nome do repositório explícito na pasta (`carf-geoapi`, etc)
- Fácil identificar qual repo é qual
- Consistência entre todos os projetos

### 2. Isolamento
- `SRC-CODE/` contém APENAS código-fonte
- Separação clara entre docs e código
- Cada repo tem seu próprio namespace

### 3. Expansibilidade
- Se precisar de múltiplas versões: `carf-geoapi-v2/`
- Se precisar de fork: `carf-geoapi-fork/`
- Se precisar de experimentos: `carf-geoapi-experimental/`

### 4. Git Submodules (Opcional Futuro)
```bash
# Se quiser usar submodules no futuro
cd /c/DEV/CARF/PROJECTS/GEOAPI/SRC-CODE
git submodule add https://github.com/org/carf-geoapi.git carf-geoapi
```

### 5. Consistência com Documentação
- `PROJECTS/GEOAPI/DOCS/` → documentação específica
- `PROJECTS/GEOAPI/SRC-CODE/carf-geoapi/` → código
- `CENTRAL/` → documentação compartilhada

---

## Estrutura Final Completa

```
C:\DEV\CARF/
├── .git                        # Repo principal (CARF monorepo docs)
├── README.md
├── .claude/
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── CENTRAL/                    # Single Source of Truth
│   ├── API/
│   ├── ARCHITECTURE/
│   │   └── ADRs/
│   ├── BUSINESS-RULES/
│   ├── DOMAIN-MODEL/
│   ├── INTEGRATION/
│   │   └── KEYCLOAK/
│   ├── OPERATIONS/
│   ├── REQUIREMENTS/
│   ├── SECURITY/
│   ├── TESTING/
│   ├── VERSIONING/
│   └── WORKFLOWS/
│
└── PROJECTS/
    ├── GEOAPI/
    │   ├── DOCS/
    │   │   ├── ARCHITECTURE/
    │   │   ├── CONCEPTS/
    │   │   ├── HOW-TO/
    │   │   └── LAYERS/
    │   └── SRC-CODE/
    │       └── carf-geoapi/    # .NET 9 Backend
    │           ├── .git/
    │           ├── src/
    │           │   ├── Domain/
    │           │   ├── Application/
    │           │   ├── Infrastructure/
    │           │   └── Gateway/
    │           └── tests/
    │
    ├── GEOWEB/
    │   ├── DOCS/
    │   │   ├── ARCHITECTURE/
    │   │   ├── CONCEPTS/
    │   │   ├── HOW-TO/
    │   │   └── LAYERS/
    │   └── SRC-CODE/
    │       └── carf-geoweb/    # React 18 Web App
    │           ├── .git/
    │           ├── src/
    │           │   ├── app/
    │           │   ├── features/
    │           │   ├── entities/
    │           │   └── shared/
    │           └── public/
    │
    ├── REURBCAD/
    │   ├── DOCS/
    │   │   ├── ARCHITECTURE/
    │   │   ├── CONCEPTS/
    │   │   ├── HOW-TO/
    │   │   └── LAYERS/
    │   └── SRC-CODE/
    │       └── carf-reurbcad/  # React Native Mobile
    │           ├── .git/
    │           ├── src/
    │           ├── android/
    │           └── ios/
    │
    ├── GEOGIS/
    │   ├── DOCS/
    │   └── SRC-CODE/
    │       └── carf-geogis/    # Python QGIS Plugin
    │           ├── .git/
    │           ├── ui/
    │           └── utils/
    │
    ├── WEBDOCS/
    │   ├── DOCS/
    │   └── SRC-CODE/
    │       └── carf-webdocs/   # VitePress Docs
    │           ├── .git/
    │           └── docs/
    │
    ├── ADMIN/
    │   ├── DOCS/
    │   └── SRC-CODE/
    │       └── carf-admin/     # Next.js Admin Console
    │           ├── .git/
    │           └── src/
    │
    └── TSCORE/
        ├── DOCS/
        └── SRC-CODE/
            └── carf-tscore/    # TypeScript Shared Library
                ├── .git/
                ├── src/
                └── package.json
```

---

## Checklist de Execução

- [ ] Backup completo antes de começar
- [ ] Reorganizar GEOAPI
- [ ] Reorganizar GEOWEB
- [ ] Reorganizar REURBCAD
- [ ] Reorganizar GEOGIS
- [ ] Reorganizar WEBDOCS
- [ ] Reorganizar ADMIN (verificar se existe)
- [ ] Reorganizar TSCORE
- [ ] Verificar que todos os .git funcionam
- [ ] Testar `git status` em cada repo
- [ ] Atualizar README.md do CARF principal com nova estrutura
- [ ] Deletar este arquivo após conclusão
