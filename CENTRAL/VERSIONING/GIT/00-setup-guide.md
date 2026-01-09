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

**1. Clone o repositório de documentação:**

```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
```

**2. Clone apenas seu projeto:**

```bash
# Escolha UM dos comandos abaixo:

# Backend Developer
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE

# Frontend Developer
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE

# Mobile Developer
git clone https://github.com/Thalesvpr/carf-reurbcad.git PROJECTS/REURBCAD/SRC-CODE

# GIS Developer
git clone https://github.com/Thalesvpr/carf-geogis.git PROJECTS/GEOGIS/SRC-CODE

# Documentation Team
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
```

**3. Siga as instruções do projeto:**

Acesse o README do projeto que você clonou:
- `PROJECTS/GEOAPI/SRC-CODE/README.md`
- `PROJECTS/GEOWEB/SRC-CODE/README.md`
- `PROJECTS/REURBCAD/SRC-CODE/README.md`
- `PROJECTS/GEOGIS/SRC-CODE/README.md`
- `PROJECTS/WEBDOCS/SRC-CODE/README.md`

## Setup Completo

### Para Tech Leads, Arquitetos e DevOps

**1. Clone o repositório de documentação:**

```bash
git clone https://github.com/Thalesvpr/carf-docs.git
cd carf-docs
```

**2. Clone todos os repositórios:**

```bash
# Backend .NET
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE

# Frontend React
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE

# Mobile React Native
git clone https://github.com/Thalesvpr/carf-reurbcad.git PROJECTS/REURBCAD/SRC-CODE

# Plugin QGIS
git clone https://github.com/Thalesvpr/carf-geogis.git PROJECTS/GEOGIS/SRC-CODE

# Portal de Documentação
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
```

**3. Verificar estrutura:**

```bash
tree -L 3 -d PROJECTS/
```

Esperado:
```
PROJECTS/
├── GEOAPI/
│   ├── DOCS/
│   └── SRC-CODE/          # ← Repositório carf-geoapi
├── GEOGIS/
│   ├── DOCS/
│   └── SRC-CODE/          # ← Repositório carf-geogis
├── GEOWEB/
│   ├── DOCS/
│   └── SRC-CODE/          # ← Repositório carf-geoweb
├── REURBCAD/
│   ├── DOCS/
│   └── SRC-CODE/          # ← Repositório carf-reurbcad
└── WEBDOCS/
    ├── DOCS/
    └── SRC-CODE/          # ← Repositório carf-webdocs
```

## Estrutura de Diretórios Explicada

```
carf-docs/                              # Repositório de documentação
├── .gitignore                          # Ignora pastas SRC-CODE/
├── README.md                           # Visão geral do projeto
│
├── CENTRAL/                            # Single Source of Truth
│   ├── REQUIREMENTS/                   # 222 requisitos funcionais
│   ├── ARCHITECTURE/                   # ADRs, deployment, patterns
│   ├── API/                            # Contratos REST
│   ├── TECHNICAL/                      # Modelo de domínio
│   ├── GIT/                            # Estratégia polyrepo (você está aqui!)
│   ├── INTEGRATION/                    # Protocolos de integração
│   └── SECURITY/                       # Políticas de segurança
│
├── PROJECTS/                           # Projetos individuais
│   ├── GEOAPI/
│   │   ├── DOCS/                       # Docs específicas do backend (versionado em carf-docs)
│   │   └── SRC-CODE/                   # Código-fonte do backend (repo independente, gitignored)
│   ├── GEOWEB/
│   │   ├── DOCS/                       # Docs específicas do frontend
│   │   └── SRC-CODE/                   # Código-fonte do frontend (repo independente, gitignored)
│   ├── REURBCAD/
│   │   ├── DOCS/                       # Docs específicas do mobile
│   │   └── SRC-CODE/                   # Código-fonte do mobile (repo independente, gitignored)
│   ├── GEOGIS/
│   │   ├── DOCS/                       # Docs específicas do plugin
│   │   └── SRC-CODE/                   # Código-fonte do plugin (repo independente, gitignored)
│   └── WEBDOCS/
│       ├── DOCS/                       # Docs específicas do portal
│       └── SRC-CODE/                   # Código-fonte do portal (repo independente, gitignored)
│
└── DEVELOPMENT/                        # Infraestrutura e operações
    └── INFRASTRUCTURE/
        └── OPERATIONS/
```

## Como o .gitignore Funciona

O arquivo `.gitignore` na raiz do `carf-docs` contém:

```gitignore
# Repositórios de código (polyrepo)
PROJECTS/GEOAPI/SRC-CODE/
PROJECTS/GEOWEB/SRC-CODE/
PROJECTS/REURBCAD/SRC-CODE/
PROJECTS/GEOGIS/SRC-CODE/
PROJECTS/WEBDOCS/SRC-CODE/
```

Isso significa:
- ✅ Pastas `PROJECTS/*/DOCS/` são versionadas no `carf-docs`
- ❌ Pastas `PROJECTS/*/SRC-CODE/` são ignoradas pelo `carf-docs`
- ✅ Cada pasta `SRC-CODE/` é um repositório Git independente
- ✅ Você pode trabalhar em múltiplos repos sem conflitos

## Workflow de Trabalho

### Cenário 1: Atualizar Documentação

```bash
# Na raiz do carf-docs
cd ~/carf-docs

# Criar branch
git checkout -b docs/atualiza-rf-001

# Editar arquivos
vim CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-001-*.md

# Commit e push
git add .
git commit -m "docs: atualiza requisito RF-001 com novos critérios"
git push origin docs/atualiza-rf-001

# Criar PR no GitHub
gh pr create --title "docs: atualiza RF-001" --body "Atualiza critérios de aceitação"
```

### Cenário 2: Desenvolver Feature no Backend

```bash
# Entre no repositório do backend
cd ~/carf-docs/PROJECTS/GEOAPI/SRC-CODE

# Criar branch
git checkout -b feature/nova-api-endpoint

# Desenvolver
vim src/Gateway/Controllers/UnitsController.cs

# Commit e push
git add .
git commit -m "feat: adiciona endpoint GET /units/search"
git push origin feature/nova-api-endpoint

# Criar PR no carf-geoapi
gh pr create --title "feat: adiciona busca de unidades" --body "Implementa RF-052"
```

### Cenário 3: Mudança Cross-Repo (Backend + Frontend)

```bash
# 1. Backend primeiro
cd ~/carf-docs/PROJECTS/GEOAPI/SRC-CODE
git checkout -b feature/new-filter-api
# ... implementa API ...
git commit -m "feat: adiciona filtro avançado de unidades"
git push origin feature/new-filter-api

# 2. Frontend depois (usando a mesma branch pattern)
cd ~/carf-docs/PROJECTS/GEOWEB/SRC-CODE
git checkout -b feature/new-filter-ui
# ... implementa UI ...
git commit -m "feat: adiciona UI para filtro avançado"
git push origin feature/new-filter-ui

# 3. Criar PRs coordenados
cd ~/carf-docs/PROJECTS/GEOAPI/SRC-CODE
gh pr create --title "feat: API filtro avançado" --body "Backend para #123"

cd ~/carf-docs/PROJECTS/GEOWEB/SRC-CODE
gh pr create --title "feat: UI filtro avançado" --body "Frontend para #124. Depende de: Thalesvpr/carf-geoapi#123"
```

### Cenário 4: Atualizar Todos os Repositórios

```bash
# Script para atualizar todos os repos
cd ~/carf-docs

# Atualizar documentação
git pull origin main

# Atualizar cada repositório de código
for project in GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS; do
  if [ -d "PROJECTS/$project/SRC-CODE/.git" ]; then
    echo "Atualizando $project..."
    cd "PROJECTS/$project/SRC-CODE"
    git pull origin main
    cd ../../..
  fi
done
```

Salve esse script como `.scripts/update-all-repos.sh` para reutilizar.

## Verificação de Saúde

### Verificar Estado de Todos os Repositórios

```bash
# Criar script de verificação
cat > .scripts/check-repos-status.sh <<'EOF'
#!/bin/bash
echo "=== CARF Docs ==="
git status -sb

for project in GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS; do
  if [ -d "PROJECTS/$project/SRC-CODE/.git" ]; then
    echo ""
    echo "=== $project ==="
    cd "PROJECTS/$project/SRC-CODE"
    git status -sb
    cd ../../..
  fi
done
EOF

chmod +x .scripts/check-repos-status.sh
.scripts/check-repos-status.sh
```

### Verificar Branches

```bash
# Ver branch atual de cada repo
for project in GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS; do
  if [ -d "PROJECTS/$project/SRC-CODE/.git" ]; then
    cd "PROJECTS/$project/SRC-CODE"
    echo "$project: $(git branch --show-current)"
    cd ../../..
  fi
done
```

## Troubleshooting

### Erro: "fatal: not a git repository"

**Problema:** Você está tentando usar comandos Git em uma pasta que não é um repositório.

**Solução:**
```bash
# Verifique se está na pasta correta
pwd

# Se estiver em PROJECTS/GEOAPI/SRC-CODE mas ela estiver vazia:
cd ~/carf-docs
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
```

### Erro: "destination path already exists"

**Problema:** Você tentou clonar um repositório que já existe.

**Solução:**
```bash
# Remova a pasta existente (cuidado!)
rm -rf PROJECTS/GEOAPI/SRC-CODE

# Clone novamente
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
```

### Conflito: "Your branch and 'origin/main' have diverged"

**Problema:** Suas mudanças locais divergiram do remoto.

**Solução:**
```bash
# Opção 1: Rebase (recomendado)
git pull --rebase origin main

# Opção 2: Merge
git pull origin main

# Opção 3: Reset (perde mudanças locais!)
git fetch origin
git reset --hard origin/main
```

### Esqueci de clonar na pasta SRC-CODE correta

**Problema:** Você clonou o repositório no lugar errado.

**Solução:**
```bash
# Mover para o local correto
mv carf-geoapi PROJECTS/GEOAPI/SRC-CODE

# Ou remover e clonar novamente
rm -rf carf-geoapi
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
```

## Próximos Passos

1. ✅ Setup concluído
2. 📖 Ler documentação específica do projeto em `PROJECTS/{PROJECT}/DOCS/README.md`
3. 🔧 Configurar ambiente de desenvolvimento (Docker, variáveis de ambiente, etc.)
4. 🏃 Executar projeto localmente
5. 🧪 Rodar testes
6. 💻 Começar a desenvolver!

## Referências

- [Polyrepo Strategy](01-polyrepo-strategy.md)
- [Branching Strategy](02-branching-strategy.md)
- [Commit Conventions](03-commit-conventions.md)
- [PR Guidelines](04-pr-guidelines.md)
- [Release Coordination](06-release-coordination.md)

---

**Última atualização:** 2026-01-08
