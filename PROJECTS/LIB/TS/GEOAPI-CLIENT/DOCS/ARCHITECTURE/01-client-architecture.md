---
type: leaf
status: active
updated: 2026-02-09
---

# Arquitetura do Cliente GEOAPI

## Visao Geral

O pacote @carf/geoapi-client usa geracao automatica de codigo via orval para criar tipos TypeScript e hooks React Query a partir do swagger.json da GEOAPI. A aplicacao consumidora (REURBWEB, REURBCAD, REURBMASTER) importa funcoes e hooks prontos, sem necessidade de implementar chamadas HTTP manualmente.

## Fluxo de Geracao

O swagger.json da GEOAPI serve como fonte de verdade. O orval le esse arquivo e gera codigo em src/generated/, organizado por tags (um arquivo por controller). O src/index.ts re-exporta os artefatos gerados junto com o client customizado e as classes de erro.

```
swagger.json → orval → src/generated/ → re-exported via index.ts
```

## Camadas

### Geracao Automatica (src/generated/)

Codigo auto-gerado pelo orval a partir do swagger.json. Contem:

- **Tipos**: interfaces TypeScript para todos os DTOs (request e response)
- **Hooks React Query**: useQuery para GETs, useMutation para POST/PUT/DELETE
- **Funcoes vanilla**: versoes sem React Query para uso em qualquer contexto

Organizado por tags do Swagger (um arquivo por dominio: units, holders, communities, documents, sync, health).

### Custom Axios Instance (src/client.ts)

Axios instance configurado que o orval usa como mutator. Responsabilidades:

- **Auth interceptor**: injeta header `Authorization: Bearer <token>` via callback `getToken()`
- **Tenant interceptor**: injeta header `X-Tenant-Id` via callback `getTenantId()`
- **Retry**: axios-retry com 3 tentativas, exponential backoff, em 5xx e erros de rede
- **Error mapping**: transforma erros HTTP em classes tipadas de src/errors.ts

### Error Mapping (src/errors.ts)

Hierarquia de erros tipados mapeados do HTTP status code:

| Status | Classe |
|:-------|:-------|
| 0 / network | NetworkError |
| 400 | ValidationError |
| 401 | AuthenticationError |
| 404 | NotFoundError |
| 409 | ConflictError |
| 500+ | ServerError |

Todas estendem ApiError (que estende Error) com campos status, code, message e details.

## Design Patterns

### Mutator Pattern (orval)

O orval aceita um custom instance como mutator — todas as chamadas geradas passam por esse axios instance, que ja contem interceptors de auth e tenant. A aplicacao consumidora nao precisa configurar headers manualmente.

### Tags-Split

O mode tags-split do orval gera um arquivo separado por tag do Swagger. Cada controller do backend (UnitsController, HoldersController, etc.) vira um modulo independente no generated/.

### Callback Injection

Auth e tenant sao injetados via callbacks (`getToken`, `getTenantId`) em vez de depender diretamente de KeycloakClient. Isso permite que cada app consumidora plugue sua propria implementacao (REURBWEB usa KeycloakClient, REURBCAD usa SecureStore adapter).

## Configuracao

A configuracao minima requer `baseURL`, `getToken` e `getTenantId`. Ver SPECS/02-client-config para a interface completa.

## Fronteira com @carf/tscore

O @carf/tscore exporta modelos de dominio completos (Unit, Holder, Community com todas as propriedades para WatermelonDB e logica offline), enums com logica de negocio (transitions, labels), auth (KeycloakClient) e validacoes de documentos (CPF, CNPJ, Email, Phone com DocumentValidationError).

O @carf/geoapi-client exporta tipos de API gerados automaticamente via orval: tipos de request (Create*Request, Update*Request), tipos de response (*Dto), hooks React Query e funcoes vanilla. Os dois pacotes nao duplicam tipos — cada um tem sua responsabilidade clara.

## Referencias

- ADRs/ADR-001-orval-code-generation: Decisao de usar orval
- SPECS/01-package-json: Dependencias e scripts
- SPECS/02-client-config: Interface de configuracao
