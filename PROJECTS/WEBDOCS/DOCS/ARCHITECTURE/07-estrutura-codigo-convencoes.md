---
type: leaf
status: review
updated: 2026-02-07
---

# Estrutura de Codigo - Convencoes

Convencoes de nomenclatura e regras de posicionamento de arquivos no WEBDOCS. Documento complementar a 07-estrutura-codigo.md.

## Arquivos de Configuracao na Raiz

| Arquivo | Proposito |
|---------|-----------|
| astro.config.mjs | Configuracao principal Astro |
| package.json | Dependencias e scripts |
| tsconfig.json | Configuracao TypeScript |
| .env.example | Template de variaveis de ambiente |
| biome.json | Configuracao do linter Biome |
| playwright.config.ts | Configuracao Playwright |
| vitest.config.ts | Configuracao Vitest |

## Convencoes de Nomenclatura

| Tipo | Padrao | Exemplos |
|------|--------|----------|
| Componentes | PascalCase.astro | StatusGrid.astro, UserMenu.astro |
| Paginas | kebab-case.astro ou [param].astro | login.astro, [...slug].astro |
| API routes | kebab-case.ts | health.ts, refresh.ts |
| Modulos lib | kebab-case.ts | pkce.ts, tokens.ts |
| Conteudo | kebab-case.mdx | primeiros-passos.mdx, cadastro-unidade.mdx |
| Estilos | kebab-case.css | custom.css |

## Onde Criar Cada Tipo de Arquivo

| Tipo de arquivo | Diretorio destino |
|----------------|-------------------|
| Nova pagina docs | src/content/docs/{secao}/ |
| Novo componente UI | src/components/{categoria}/ |
| Nova rota API | src/pages/api/ |
| Nova funcao util | src/lib/{dominio}/ |
| Novo estilo | src/styles/ |
| Nova imagem | public/images/ |
| Novo teste E2E | tests/e2e/ |
| Novo teste unitario | tests/unit/ |
