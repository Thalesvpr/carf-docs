---
type: leaf
status: review
updated: 2026-02-07
---

# OIDC - UserInfo, JWKS, Logout, Introspection e Revocation

Endpoints complementares do protocolo OpenID Connect no realm CARF.

## UserInfo Endpoint

O endpoint GET /protocol/openid-connect/userinfo retorna claims do usuario autenticado mediante Bearer token. A resposta inclui sub, email_verified, name, preferred_username (CPF), given_name, family_name, email, tenant_id, allowed_tenants, community_ids e realm_access com roles.

## JWKS Endpoint

O endpoint GET /protocol/openid-connect/certs retorna chaves publicas RSA para validacao de assinatura JWT. A resposta contem array keys com kid, kty RSA, alg RS256, use sig, n (modulus) e e (exponent). Cachear chaves por 10 minutos e usar kid do header JWT para selecionar a chave correta.

## Logout Endpoint

O endpoint GET /protocol/openid-connect/logout encerra a sessao SSO.

| Parametro | Descricao |
|:----------|:----------|
| id_token_hint | ID token para identificar sessao |
| post_logout_redirect_uri | URI para redirect apos logout |
| state | Valor opaco retornado no redirect |

Para back-channel logout, enviar POST com client_id e refresh_token.

## Introspection Endpoint

O endpoint POST /protocol/openid-connect/token/introspect valida token e retorna claims. Requer autenticacao do client. Enviar token, token_type_hint, client_id e client_secret. Token valido retorna active true com claims completas. Token invalido retorna apenas active false.

## Revocation Endpoint

O endpoint POST /protocol/openid-connect/revoke invalida refresh token especifico. Enviar token, token_type_hint e client_id. Retorna 200 OK sempre.

## Estrutura do Access Token JWT

O header contem alg RS256, typ JWT e kid. O payload contem exp, iat, jti, iss (issuer), aud, sub (UUID), typ Bearer, azp (client), session_state, realm_access com roles, resource_access, scope, email_verified, name, preferred_username (CPF), email, tenant_id, allowed_tenants e community_ids.

Ver [02-oidc-endpoints](./02-oidc-endpoints.md) para discovery, authorization e token endpoints.
