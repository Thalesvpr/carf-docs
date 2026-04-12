---
type: leaf
status: active
updated: 2026-02-09
---

# Authentication Flow - @carf/geoapi-client

## Fluxo de Autenticacao

O geoapi-client desacopla a autenticacao via callbacks. A aplicacao consumidora fornece duas funcoes na configuracao:

- `getToken(): Promise<string>` — retorna o JWT access token atual
- `getTenantId(): string` — retorna o ID do tenant ativo

O client nao conhece Keycloak, SecureStore ou qualquer provider de auth diretamente. Cada app consumidora injeta sua propria implementacao.

## Interceptors

### Request Interceptor de Auth

Antes de cada requisicao, o interceptor chama `getToken()` e injeta o header `Authorization: Bearer <token>`. Se `getToken()` lanca erro (token expirado e refresh falhou), o request falha com AuthenticationError.

### Request Interceptor de Tenant

Injeta o header `X-Tenant-Id` com o valor retornado por `getTenantId()` em todas as requisicoes.

## Refresh e Retry em 401

Se o backend retorna 401, a responsabilidade de refresh e da funcao `getToken()` fornecida pela aplicacao. O padrao recomendado:

1. `getToken()` verifica se o token esta expirado
2. Se expirado, faz refresh automaticamente (via KeycloakClient no REURBWEB, via SecureStore adapter no REURBCAD)
3. Retorna o novo token

O axios-retry nao retenta 401 automaticamente (e um erro 4xx). Se a app precisa de retry apos refresh, deve implementar essa logica no proprio `getToken()`.

## Configuracao por App

### REURBWEB (React/Next.js)

O REURBWEB usa KeycloakClient do @carf/tscore. A funcao getToken delega para keycloakClient.getAccessToken que gerencia cache e refresh. A funcao getTenantId busca o tenantId do contexto do usuario autenticado.

### REURBCAD (React Native/Expo)

O REURBCAD usa SecureStore para armazenar tokens e um adapter que implementa a mesma interface. A funcao getToken busca do SecureStore e faz refresh se necessario. A funcao getTenantId busca do AsyncStorage.

## Seguranca

- PKCE e usado nos public clients (REURBWEB, REURBCAD) para prevenir interceptacao
- Em producao, todas as URLs devem usar HTTPS
- Tokens sao armazenados de forma segura por cada app consumidora (localStorage para web, SecureStore para mobile)
