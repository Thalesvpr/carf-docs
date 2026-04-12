---
type: adr
status: accepted
updated: 2026-02-09
---

# ADR-001: Geracao Automatica de Cliente via Orval

## Status

Aceito

## Contexto

O pacote @carf/geoapi-client foi projetado como um cliente HTTP artesanal com 13 APIs de dominio, interceptors, circuit breaker e classes de endpoint manuais. Essa implementacao nunca foi concretizada — o src/index.ts exporta modulos inexistentes. A GEOAPI backend ja expoe swagger.json via Swashbuckle, e a API esta em evolucao ativa com novos endpoints sendo adicionados regularmente.

Manter um cliente artesanal sincronizado manualmente com o backend nao escala: cada novo endpoint ou alteracao de DTO exigiria mudancas coordenadas em dois repositorios.

## Decisao

Usar o **orval** para gerar automaticamente tipos TypeScript e hooks React Query a partir do swagger.json da GEOAPI.

### Arquitetura resultante

- **swagger.json** (fonte de verdade) → **orval** (gerador) → **src/generated/** (codigo auto-gerado)
- **src/client.ts**: axios instance customizado com interceptors de auth e tenant via callbacks
- **src/errors.ts**: hierarquia de erros tipados mapeados de HTTP status codes
- **src/index.ts**: re-exporta generated + client + errors

### Configuracao orval

- **Mode**: tags-split (um arquivo por tag/controller do Swagger)
- **Client**: react-query para hooks, funcoes vanilla para uso sem React
- **Mutator**: custom axios instance (src/client.ts) injetado em todas as chamadas

## Alternativas Consideradas

### openapi-typescript-codegen

Gera classes de servico e tipos. Projeto com manutencao inconsistente. Nao gera hooks React Query nativamente.

### swagger-typescript-api

Gera cliente Axios completo. Mais opinado que o orval, menos flexivel no output. Nao tem suporte nativo a React Query.

### Implementacao manual

Conforme planejado originalmente. Exigiria manter 13+ classes de endpoint, dezenas de DTOs e testes unitarios em sincronia manual com o backend. Inviavel para equipe pequena com API em evolucao.

## Consequencias

### Positivas

- Types e hooks sempre sincronizados com o backend — basta rodar `bun run generate`
- Novos endpoints no backend refletem automaticamente no client apos regeneracao
- Menos codigo manual = menos bugs de sincronia
- Hooks React Query prontos para uso no REURBWEB

### Negativas

- Types/DTOs vem do swagger, nao do @carf/tscore — pode haver divergencia de nomenclatura
- Codigo gerado pode ser verboso ou nao idiomatico
- Dependencia de ferramenta externa (orval) para build do pacote

### Mitigacoes

- Re-export seletivo no index.ts para expor apenas tipos relevantes
- Futuro sync-adapter para REURBCAD pode mapear tipos gerados para formato WatermelonDB
- Swagger annotations no backend controlam qualidade do output gerado
