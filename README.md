# CARF WEBDOCS

Portal de documentação estático do sistema CARF gerado com VitePress a partir dos markdown em CENTRAL e TECHNICAL.

## Descrição

Site estático para documentação pública do sistema CARF, consumindo automaticamente os arquivos markdown do repositório carf-docs e gerando navegação hierárquica com sidebar, busca full-text e temas claro/escuro.

## Estrutura

- **.vitepress/**: Configuração VitePress (config.js, theme customizations)
- **public/**: Assets estáticos (imagens, logos)
- **scripts/**: Scripts automação (sync docs, filter private content)
- **docs/**: Documentação processada (gerado automaticamente)

## Stack Tecnológica

- VitePress
- Vue 3
- Node.js 20+
- GitHub Actions (CI/CD)

## Funcionalidades

- Geração automática navegação a partir estrutura pastas CENTRAL
- Busca full-text integrada
- Syntax highlighting código
- Diagrams Mermaid
- Responsive design
- Temas claro/escuro
- Deploy automático GitHub Pages ou S3

## Requisitos

- Node.js 20+
- npm ou yarn

## Comandos

```bash
# Instalar dependências
npm install

# Dev server (hot reload)
npm run dev

# Build production
npm run build

# Preview build
npm run preview

# Sync docs do carf-docs repo
npm run sync-docs
```

## Configuração

O arquivo `.vitepress/config.js` define:

- Sidebar structure (navegação)
- Plugins (search, mermaid, etc)
- Theme customizations
- Base URL deploy
- Meta tags SEO

## Deploy

### GitHub Actions (automatizado)

Push para `main` dispara workflow que:
1. Executa `npm run sync-docs` (filtra docs privadas)
2. Build VitePress (`npm run build`)
3. Deploy GitHub Pages ou S3

### Manual

```bash
# Build
npm run build

# Deploy GitHub Pages
npm run deploy

# Ou upload dist/ para S3/Netlify/Vercel
```

## Filtragem Conteúdo Privado

Script `scripts/filter-private.js` remove automaticamente:
- Credenciais, IPs internos
- Arquivos marcados com `private: true` no frontmatter YAML
- Seções sensíveis (SECURITY/INCIDENTS/, etc)

## Documentação

Ver pasta `PROJECTS/WEBDOCS/` no repositório carf-docs para detalhes configuração e customização.

## Licença

Proprietário - Uso restrito
