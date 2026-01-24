---
type: leaf
status: review
updated: 2026-01-24
---

# Package.json

Especificacao do package.json da biblioteca @carf/tscore definindo metadados, dependencias e configuracao de publicacao.

## Metadados

O campo name define @carf/tscore com escopo @carf para GitHub Packages. Campo version segue semver comecando em 0.1.0 durante desenvolvimento. Campo description resume proposito da biblioteca. Campo repository aponta para repositorio GitHub. Campo license define MIT. Campo main aponta para dist/index.js e types para dist/index.d.ts como entry points.

## Exports Map

Campo exports define subpath exports permitindo importacoes modulares. O path raiz exporta indice principal. Path /validations exporta value objects. Path /types exporta interfaces e enums. Path /auth exporta KeycloakClient. Paths /auth/react e /auth/vue exportam integracao de framework. Cada entry define import para JavaScript e types para declarations.

## Dependencias

Campo dependencies inclui apenas zod como dependencia runtime para schemas. Campo peerDependencies lista react e vue como opcionais. Campo peerDependenciesMeta marca ambos como optional true permitindo instalacao parcial. Campo devDependencies inclui typescript, bun-types, eslint e tipos para desenvolvimento.

## Scripts

Script build executa bun build para JavaScript seguido de tsc --emitDeclarationOnly para declarations. Script dev pode usar --watch para recompilacao. Script test executa bun test. Script typecheck executa tsc --noEmit para validacao. Script prepublishOnly executa build garantindo artefatos atualizados antes de publicar.

## Publicacao

Campo publishConfig define registry como https://npm.pkg.github.com para GitHub Packages. Campo files lista dist/ e README.md para inclusao no pacote publicado excluindo fontes e testes.

## Engines

Campo engines especifica node >=18.0.0 como versao minima para compatibilidade com ES modules e exports field. Bun 1.0 ou superior recomendado para desenvolvimento.
