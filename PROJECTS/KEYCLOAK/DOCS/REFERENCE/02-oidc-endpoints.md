---
type: leaf
status: review
updated: 2026-02-07
---

# OpenID Connect Endpoints

OIDC endpoints do realm CARF seguem a especificacao OpenID Connect Core 1.0. Base URL: /realms/carf/protocol/openid-connect.

## Discovery Document

O endpoint GET /.well-known/openid-configuration retorna metadados do provedor OIDC incluindo issuer, authorization_endpoint, token_endpoint, userinfo_endpoint, end_session_endpoint, jwks_uri, introspection_endpoint e revocation_endpoint. Grant types suportados sao authorization_code, refresh_token e client_credentials. Scopes incluem openid, profile, email, roles e carf-tenant.

## Authorization Endpoint

O endpoint GET /protocol/openid-connect/auth inicia o fluxo Authorization Code, redirecionando para tela de login.

| Parametro | Obrigatorio | Descricao |
|:----------|:------------|:----------|
| response_type | Sim | Valor code para Authorization Code |
| client_id | Sim | ID do client registrado |
| redirect_uri | Sim | URI de callback registrada |
| scope | Sim | Scopes separados por espaco |
| state | Recomendado | Valor opaco para CSRF |
| code_challenge | PKCE | Challenge gerado |
| code_challenge_method | PKCE | S256 recomendado |
| nonce | OpenID | Prevenir replay attacks |
| prompt | Opcional | login, consent ou none |
| login_hint | Opcional | Pre-preenchimento do username |

Apos autenticacao, redireciona para redirect_uri com code e state. Em erro, redireciona com error, error_description e state.

## Token Endpoint

O endpoint POST /protocol/openid-connect/token troca authorization code por tokens. Content type application/x-www-form-urlencoded.

Para Authorization Code grant, enviar grant_type, code, redirect_uri, client_id e code_verifier. Para Refresh Token, enviar grant_type, refresh_token e client_id. Para Client Credentials, enviar grant_type, client_id e client_secret. A resposta retorna access_token, expires_in, refresh_token, token_type Bearer, id_token e scope.

Ver [02a-oidc-userinfo-jwks](./02a-oidc-userinfo-jwks.md) para userinfo, JWKS, logout, introspection e revocation.
