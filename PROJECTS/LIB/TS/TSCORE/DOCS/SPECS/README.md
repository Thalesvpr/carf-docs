---
type: readme
status: review
updated: 2026-01-24
---

# Especificacoes Tecnicas

Configuracoes de projeto necessarias para desenvolvimento, build e publicacao da biblioteca @carf/tscore no GitHub Packages.

A especificacao do [package.json](./01-package-json.md) define dependencias, exports map e metadados de publicacao. O documento detalha peer dependencies opcionais para React e Vue, configuracao do registry @carf e scripts de build usando Bun. A especificacao do [tsconfig](./02-tsconfig.md) estabelece configuracoes do compilador TypeScript para geracao de ES modules e declarations. O documento cobre target ES2020, module resolution bundler e paths aliases.

O [exports map](./03-exports-map.md) documenta subpath exports que permitem importacoes modulares como @carf/tscore/validations e @carf/tscore/auth/react. Esta configuracao habilita tree-shaking e permite que projetos consumidores carreguem apenas os modulos necessarios.

A biblioteca requer Node 18 ou superior e Bun 1.0 para desenvolvimento local. Build gera ES modules em dist/ com declarations .d.ts para suporte a IDE. Publicacao ocorre automaticamente via GitHub Actions quando tags vX.X.X sao criadas.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
