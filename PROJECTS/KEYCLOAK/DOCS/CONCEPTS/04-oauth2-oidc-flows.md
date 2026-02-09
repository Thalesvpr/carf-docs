---
type: leaf
status: approved
updated: 2026-02-07
---

# OAuth2 e OpenID Connect Flows

OAuth2 e OpenID Connect sao os protocolos de autenticacao e autorizacao implementados pelo Keycloak para o ecossistema CARF. Cada tipo de aplicacao utiliza o flow adequado ao seu modelo de ameacas conforme ADR-002.

## Authorization Code com PKCE

Este e o flow principal usado por SPAs (GEOWEB, ADMIN, WEBDOCS) e mobile apps (REURBCAD). O frontend redireciona para o authorization endpoint do Keycloak incluindo client_id, redirect_uri, response_type code, scopes (openid profile email carf-tenant) e os parametros PKCE: code_challenge (hash SHA-256 base64url do code_verifier) e code_challenge_method S256. O code_verifier e um valor aleatorio de 43 a 128 caracteres armazenado em sessionStorage.

Apos autenticacao do usuario, o Keycloak redireciona de volta para a redirect_uri com authorization code e state na URL. O frontend troca o code por tokens via POST ao token endpoint enviando grant_type authorization_code, code, redirect_uri, client_id e code_verifier (sem client_secret pois e public client). O Keycloak verifica o hash do code_verifier contra o code_challenge original e, se valido, retorna access_token JWT RS256 (valido 5 minutos), refresh_token (valido conforme SSO session), id_token com informacoes do usuario, token_type Bearer e scope concedido.

## Client Credentials

Usado pelo GEOGIS para comunicacao M2M sem contexto de usuario. O servico envia POST ao token endpoint com grant_type client_credentials, client_id e client_secret via Basic Auth ou form-encoded. A resposta contem apenas access_token sem refresh_token nem id_token, pois o token representa a aplicacao e nao um usuario.

## Refresh Token

O flow de refresh mantem sessao ativa sem solicitar credenciais novamente. Antes do access token expirar, o frontend envia POST ao token endpoint com grant_type refresh_token, refresh_token e client_id, obtendo novos tokens com claims atualizados e sessao renovada. O processo repete-se ate o idle timeout ou absolute timeout serem atingidos.

## Estrutura do JWT Access Token

O header contem alg RS256 (algoritmo de assinatura), typ JWT e kid (key ID para localizar chave publica no JWKS endpoint). O payload contem claims padrao OIDC (sub UUID do usuario, iss URL do realm, aud client_id, exp timestamp de expiracao, iat timestamp de emissao) e claims customizados do scope carf-tenant (tenant_id, allowed_tenants, community_ids). Roles do realm ficam em realm_access.roles e roles por client em resource_access. A assinatura e gerada com chave privada RSA do Keycloak e validavel com chave publica exposta no JWKS endpoint, garantindo integridade sem necessidade de chamar o Keycloak para cada request (validacao stateless).

## Endpoints OIDC

O **OIDC Discovery** em /.well-known/openid-configuration retorna JSON com todos os endpoints, grant types suportados, scopes e algorithms, permitindo configuracao automatica de clients OIDC. O **Authorization Endpoint** em /protocol/openid-connect/auth inicia o flow de login. O **Token Endpoint** em /protocol/openid-connect/token processa trocas de code e refresh.

O **UserInfo Endpoint** em /protocol/openid-connect/userinfo retorna claims do usuario autenticado via Bearer header, util para obter informacoes atualizadas sem decodificar JWT. O **JWKS Endpoint** em /protocol/openid-connect/certs expoe chaves publicas RSA para validacao de assinatura. O **Introspect Endpoint** em /protocol/openid-connect/token/introspect valida tokens server-side retornando active true ou false.

O **End Session Endpoint** em /protocol/openid-connect/logout encerra sessao SSO invalidando todos tokens em todos clients simultaneamente, com redirect de volta para a aplicacao. O **Revoke Endpoint** em /protocol/openid-connect/revoke invalida refresh token especifico forcando re-autenticacao.

## Bibliotecas de Integracao

Todos os flows seguem RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), RFC 8252 (OAuth for Native Apps) e OpenID Connect Core 1.0, garantindo interoperabilidade com bibliotecas padrao. O CARF utiliza @carf/tscore KeycloakClient para TypeScript (web e React Native), python-keycloak para GEOGIS e Microsoft.AspNetCore.Authentication.JwtBearer para GEOAPI .NET.
