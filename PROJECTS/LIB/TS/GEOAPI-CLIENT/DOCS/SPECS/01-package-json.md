---
type: leaf
status: active
updated: 2026-02-09
---

# Package.json - @carf/geoapi-client

Configuracao do package.json para o cliente HTTP auto-gerado da GEOAPI.

## Metadados do Pacote

| Propriedade | Valor |
|:------------|:------|
| name | @carf/geoapi-client |
| version | 0.1.0 |
| description | Cliente HTTP auto-gerado via orval para a GEOAPI do ecossistema CARF |
| type | module |
| main | ./dist/index.js |
| types | ./dist/index.d.ts |
| license | UNLICENSED |
| author | CARF Team |
| node engine | >= 18.0.0 |

O campo exports mapeia "." para types ./dist/index.d.ts e import ./dist/index.js. O campo files inclui dist e README.md.

## Dependencias de Producao

| Pacote | Versao | Justificativa |
|:-------|:-------|:--------------|
| axios | ^1.6.0 | Cliente HTTP base para o custom instance |
| axios-retry | ^4.0.0 | Retry automatico com exponential backoff |

## Peer Dependencies

| Pacote | Versao | Obrigatorio | Justificativa |
|:-------|:-------|:------------|:--------------|
| @carf/tscore | ^0.1.0 | Sim | Types compartilhados do ecossistema |
| @tanstack/react-query | ^5.0.0 | Nao (opcional) | Necessario apenas para hooks React Query |

## Dependencias de Desenvolvimento

| Pacote | Versao | Uso |
|:-------|:-------|:----|
| orval | ^7.0.0 | Geracao automatica de tipos e hooks a partir do swagger.json |
| typescript | ^5.3.0 | Compilador e type checking |
| @types/node | ^20.10.0 | Types Node.js |
| bun-types | latest | Types Bun runtime |

## Scripts

| Script | Comando | Descricao |
|:-------|:--------|:----------|
| generate | orval --config orval.config.ts | Gera tipos e hooks a partir do swagger.json |
| swagger:fetch | curl -o swagger.json http://localhost:5127/swagger/v1/swagger.json | Baixa swagger.json atualizado da API local |
| build | bun run generate && bun build src/index.ts --outdir dist --target node | Gera codigo e compila |
| build:types | tsc --emitDeclarationOnly --declaration --declarationMap | Gera declaracoes TypeScript |
| build:all | bun run build && bun run build:types | Build completo |
| typecheck | tsc --noEmit | Verificacao de tipos sem emitir |

## Estrutura de Arquivos

O diretorio src contem:

- **index.ts**: entry point, re-exporta generated + client + errors
- **client.ts**: factory do axios instance customizado (mutator do orval)
- **errors.ts**: hierarquia de erros tipados
- **generated/**: codigo auto-gerado pelo orval (gitignored)

Na raiz do pacote:

- **orval.config.ts**: configuracao do orval
- **swagger.json**: snapshot do OpenAPI spec da GEOAPI
- **tsconfig.json**: configuracao TypeScript

## Instalacao em Projetos Consumidores

Instalar via `bun add @carf/geoapi-client`. Para usar hooks React Query, tambem instalar `@tanstack/react-query`.
