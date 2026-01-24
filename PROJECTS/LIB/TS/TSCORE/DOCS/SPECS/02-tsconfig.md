---
type: leaf
status: review
updated: 2026-01-24
---

# TSConfig

Especificacao do tsconfig.json da biblioteca @carf/tscore definindo configuracoes do compilador TypeScript.

## Target e Module

Campo target define ES2022 para suporte a features modernas como optional chaining, nullish coalescing e top-level await. Campo module define ESNext para ES modules nativos. Campo moduleResolution define bundler para resolucao compativel com bundlers modernos como Vite, esbuild e Bun.

## Paths e Directories

Campo baseUrl define ponto raiz para resolucao de modulos. Campo paths pode definir aliases como @/* mapeando para src/*. Campo outDir define dist/ como destino de compilacao. Campo rootDir define src/ como fonte.

## Declaracoes

Campo declaration true gera arquivos .d.ts com tipos para consumidores. Campo declarationMap true gera sourcemaps para declarations permitindo navegacao para fontes. Campo sourceMap true gera sourcemaps para JavaScript facilitando debug.

## Strict Mode

Campo strict true habilita todas verificacoes estritas. Campo strictNullChecks previne acesso a valores potencialmente null ou undefined. Campo noImplicitAny requer tipos explicitos em parametros. Campo noUnusedLocals e noUnusedParameters alertam sobre codigo morto. Campo noUncheckedIndexedAccess adiciona undefined a acessos por indice.

## Interoperabilidade

Campo esModuleInterop true permite imports default de modulos CommonJS. Campo allowSyntheticDefaultImports true permite sintaxe import X from para modulos sem default export. Campo resolveJsonModule true permite importar arquivos JSON. Campo isolatedModules true garante compatibilidade com transpilacao por arquivo.

## Inclusao e Exclusao

Campo include define src/**/* como arquivos fonte. Campo exclude remove node_modules, dist e arquivos de teste da compilacao. Configuracao otimizada para biblioteca publicada com types e sourcemaps completos.
