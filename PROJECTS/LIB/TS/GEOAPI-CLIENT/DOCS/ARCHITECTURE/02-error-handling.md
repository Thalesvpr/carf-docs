---
type: leaf
status: active
updated: 2026-02-09
---

# Error Handling - @carf/geoapi-client

## Sistema de Tratamento de Erros

Erros HTTP sao transformados em classes tipadas pela funcao `mapAxiosError` no response interceptor do axios instance. A aplicacao consumidora trata erros via try-catch verificando instanceof da classe especifica.

## Hierarquia de Erros

Todas as classes estendem ApiError, que estende Error.

| Classe | Status HTTP | Quando |
|:-------|:-----------|:-------|
| NetworkError | 0 | Sem conectividade ou timeout |
| ValidationError | 400 | Dados invalidos (detalhes em `details`) |
| AuthenticationError | 401 | Token invalido ou expirado |
| NotFoundError | 404 | Recurso nao encontrado |
| ConflictError | 409 | Conflito de versao ou duplicata |
| ServerError | 500+ | Erro interno do servidor |

### Classe ApiError

| Propriedade | Tipo | Descricao |
|:------------|:-----|:----------|
| status | number | Codigo HTTP (0 para erros de rede) |
| code | string ou undefined | Codigo de erro do backend (ex: UNIT_NOT_FOUND) |
| message | string | Mensagem descritiva |
| details | Record ou undefined | Campos extras (ex: erros de validacao por campo) |

## Retry Logic

O retry usa axios-retry configurado no custom axios instance:

- **Tentativas**: 3 (configuravel via `retryAttempts`)
- **Backoff**: exponencial (1s, 2s, 4s)
- **Condicoes**: erros de rede (sem resposta) e status 5xx
- **Nao retenta**: erros 4xx (client errors)

## Codigos de Erro do Backend

### 4xx - Client Errors

| Codigo | Status | Descricao |
|:-------|:-------|:----------|
| UNIT_NOT_FOUND | 404 | Unidade nao encontrada |
| HOLDER_NOT_FOUND | 404 | Posseiro nao encontrado |
| INVALID_CPF | 400 | CPF invalido |
| INVALID_COORDINATES | 400 | Coordenadas geograficas invalidas |
| UNIT_CODE_DUPLICATE | 409 | Codigo de unidade ja existe |
| UNAUTHORIZED | 401 | Token invalido ou expirado |
| FORBIDDEN | 403 | Sem permissao para esta operacao |
| VALIDATION_ERROR | 422 | Erro de validacao (detalhes em details) |

### 5xx - Server Errors

| Codigo | Status | Descricao |
|:-------|:-------|:----------|
| INTERNAL_ERROR | 500 | Erro interno do servidor |
| DATABASE_ERROR | 500 | Erro de acesso ao banco |
| SERVICE_UNAVAILABLE | 503 | Servico temporariamente indisponivel |

### Network Errors

| Codigo | Status | Descricao |
|:-------|:-------|:----------|
| NETWORK_ERROR | 0 | Sem resposta do servidor |
| TIMEOUT | 0 | Request excedeu timeout |
