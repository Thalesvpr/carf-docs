---
type: leaf
status: active
updated: 2026-02-09
---

# HTTP Client - Custom Axios Instance

## Visao Geral

O @carf/geoapi-client usa o **custom instance pattern do orval**: um axios instance pre-configurado que serve como mutator para todas as chamadas geradas. Em vez de um wrapper elaborado sobre Axios, o client.ts exporta uma factory function que cria e configura a instancia.

## Custom Instance (Mutator)

O orval aceita um "mutator" — uma funcao que recebe a config do request e retorna uma Promise com a resposta. O `customInstance` exportado por `src/client.ts` e essa funcao: ela usa o axios instance configurado internamente para executar o request.

Todas as chamadas geradas pelo orval (hooks React Query e funcoes vanilla) passam por esse mutator automaticamente.

## Configuracao

A factory `createApiClient(config)` aceita:

| Propriedade | Tipo | Obrigatorio | Padrao | Descricao |
|:------------|:-----|:------------|:-------|:----------|
| baseURL | string | Sim | -- | URL base da API |
| getToken | () => Promise<string> | Sim | -- | Callback que retorna JWT token |
| getTenantId | () => string | Sim | -- | Callback que retorna tenant ID |
| timeout | number | Nao | 30000 | Timeout em ms |
| retryAttempts | number | Nao | 3 | Tentativas de retry |
| headers | Record<string, string> | Nao | {} | Headers adicionais |

## Interceptors Built-in

### Request: Auth

Chama `getToken()` e adiciona `Authorization: Bearer <token>` a cada request. Se getToken falha (token expirado e sem refresh), o request e rejeitado.

### Request: Tenant

Adiciona `X-Tenant-Id: <tenantId>` via `getTenantId()` a cada request.

### Response: Error Mapping

Transforma erros Axios em classes tipadas (ApiError, NetworkError, ValidationError, etc.) via funcao `mapAxiosError`. A aplicacao consumidora recebe erros tipados em vez de AxiosError generico.

### Retry

axios-retry configurado com exponential backoff. Retenta erros de rede e 5xx, nao retenta 4xx.

## Uso pelo Orval

O `orval.config.ts` referencia o custom instance como mutator:

```typescript
mutator: {
  path: './src/client.ts',
  name: 'customInstance',
}
```

Com isso, todo codigo gerado automaticamente usa o axios instance configurado com auth, tenant e retry.

## Links Relacionados

- ARCHITECTURE/01-client-architecture: Arquitetura geral
- ARCHITECTURE/02-error-handling: Hierarquia de erros
- SPECS/02-client-config: Interface de configuracao completa
