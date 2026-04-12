---
type: leaf
status: review
updated: 2026-01-24
---

# Exports Map

Especificacao do exports map em package.json que habilita subpath exports para importacoes modulares da biblioteca @carf/tscore.

## Conceito de Subpath Exports

Node.js 12.7+ suporta campo exports em package.json definindo pontos de entrada publicos. Subpath exports mapeiam caminhos de importacao para arquivos internos. Consumidores importam de subpaths semanticos sem conhecer estrutura interna do pacote.

## Estrutura do Exports

O path raiz ponto exporta dist/index.js como import e dist/index.d.ts como types. Path /validations exporta dist/validations/index.js e types correspondente para value objects. Path /types exporta dist/types/index.js para interfaces e enums. Path /auth exporta dist/auth/index.js para cliente base. Paths /auth/react e /auth/vue exportam integracao especifica de framework.

## Beneficios para Consumidores

Importacoes semanticas como @carf/tscore/validations comunicam intencao claramente. Tree-shaking elimina codigo nao utilizado quando bundler analisa imports especificos. Projetos React importam apenas /auth/react sem carregar codigo Vue. Projetos que usam apenas tipos importam /types com custo zero de bundle.

## Condicoes de Export

Cada entry define import para ES modules e types para declarations TypeScript. Condicao import atende imports dinamicos e estaticos em runtime. Condicao types atende compilador TypeScript e language servers para autocomplete e validacao.

## Restricao de Acesso

Subpath exports implicitamente bloqueiam acesso a arquivos nao listados. Consumidores nao podem importar de caminhos internos como dist/internal/helper.js se path nao esta em exports. Esta restricao protege detalhes de implementacao e permite refatoracao interna sem breaking changes.

## Compatibilidade

Bundlers modernos como Vite, esbuild e webpack 5 suportam exports nativamente. TypeScript 4.7+ resolve types via exports com moduleResolution bundler ou node16. Node.js 18+ recomendado para suporte completo.
