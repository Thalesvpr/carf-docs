---
type: leaf
status: review
updated: 2026-01-24
---

# Estrutura de Pacote

Organizacao interna do pacote @carf/tscore descrevendo diretorios, modulos e exports publicos.

## Diretorio Source

O diretorio src/ organiza codigo em quatro modulos principais. O diretorio types/ contem subdiretorios domain/ com entidades Unit, Holder e Community, api/ com tipos de request e response, e common/ com utilitarios como paginacao e Result. O diretorio validations/ contem classes CPF, CNPJ, Email e Phone implementando value objects com ValidationError.

O diretorio auth/ contem KeycloakClient com logica OAuth2 PKCE, subdiretorios react/ e vue/ com integracao especifica de framework, e adapters/ com interfaces StorageAdapter e NavigationAdapter para abstracao de plataforma. O diretorio constants/ define enums Status e Roles compartilhados.

## Exports Publicos

O arquivo index.ts re-exporta seletivamente APIs publicas de cada modulo. O package.json define exports map mapeando subpaths para arquivos de distribuicao. O path principal exporta tudo. O path /validations exporta apenas value objects. O path /types exporta interfaces e enums. O path /auth exporta KeycloakClient. Os paths /auth/react e /auth/vue exportam integracao de framework.

## Build Output

O diretorio dist/ contem JavaScript transpilado como ES modules e arquivos .d.ts com declarations TypeScript. Sourcemaps vinculam codigo transpilado a fontes originais para debugging. A estrutura de diretorios espelha src/ mantendo subpath exports funcionais.

## Desenvolvimento

Scripts npm definem build com Bun para JavaScript e tsc para declarations. Script dev executa TypeScript com watch mode. Script test executa suite Bun. Script typecheck valida tipos sem emitir arquivos. Desenvolvimentos locais usam npm link para consumo em projetos dependentes.
