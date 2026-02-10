---
type: leaf
status: review
updated: 2026-02-07
---

# Tooling e Configuracao

Arquivos de configuracao de ferramentas do projeto WEBDOCS. Arquivo relacionado com 25a-package-json.md.

## tsconfig.json

Estende astro/tsconfigs/strict. BaseUrl na raiz com path aliases: @ para src/*, @components para src/components/*, @lib para src/lib/*, @config para src/config/*, @content para src/content/*. JSX configurado com react-jsx e jsxImportSource react. Types incluem astro/client e vite/client. Opcoes strict habilitadas: strictNullChecks, noUnusedLocals, noUnusedParameters, noImplicitReturns, noFallthroughCasesInSwitch e forceConsistentCasingInFileNames. Include para src e tests, exclude para node_modules e dist.

## biome.json

Schema versao 1.9.0. Organize imports habilitado. Linter habilitado com regras recommended, complexity noExcessiveCognitiveComplexity como warn, correctness noUnusedImports e noUnusedVariables como error, style useConst como error e noNonNullAssertion como warn. Formatter com indentStyle space, indentWidth 2, lineWidth 100. JavaScript formatter com quoteStyle single, trailingCommas es5, semicolons always. Arquivos ignorados: node_modules, dist, .astro, public/admin.

## playwright.config.ts

TestDir em ./tests/e2e. FullyParallel habilitado. ForbidOnly ativo em CI. Retries 2 em CI e 0 local. Workers 1 em CI. Reporter html. BaseURL http://localhost:4321. Trace on-first-retry. Projetos para chromium (Desktop Chrome), firefox (Desktop Firefox), webkit (Desktop Safari) e Mobile Chrome (Pixel 5). WebServer usando bun run preview na porta 4321, reuseExistingServer quando nao CI.

## vitest.config.ts

Usa getViteConfig do astro/config. Testes incluem tests/unit/**/*.test e spec em js e ts. Globals habilitado. Environment node. Coverage com provider v8, reporters text json e html, include para src/lib/**/*.ts, exclude para arquivos .d.ts.

## Instalacao e Atualizacao

Para projeto novo, criar diretorio carf-webdocs, copiar package.json, executar bun install, copiar arquivos de configuracao (tsconfig.json, biome.json, playwright.config.ts, vitest.config.ts), e verificar com bun run check.

Para atualizar dependencias, usar bun outdated para ver desatualizadas, bun update para atualizar todas, ou bun update astro para atualizar especifica.
