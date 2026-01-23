---
type: leaf
status: current
updated: 2026-01-22
---

# Authentication

Padrao de autenticacao centralizada via Keycloak para todos os sistemas do ecossistema CARF usando OAuth2 e OpenID Connect. Cada sistema obtem tokens JWT que sao validados pela GEOAPI em cada requisicao.

Fluxo Authorization Code com PKCE e usado por aplicacoes com usuario interativo. GEOWEB e ADMIN redirecionam para Keycloak, usuario autentica, e retorna com authorization code trocado por tokens. REURBCAD usa custom URL scheme para capturar callback. GEOGIS usa servidor HTTP local temporario no desktop.

## Tokens

Access token JWT de curta duracao (15 minutos) contem claims de identidade, roles e tenant_id. Refresh token de longa duracao (8 horas mobile, 30 minutos web) permite renovar access token sem reautenticar. ID token fornece informacoes de perfil do usuario para exibicao na interface.
