---
type: leaf
status: review
updated: 2026-02-07
---

# Authentication

Padrao de autenticacao centralizada via Keycloak para todos os sistemas do ecossistema CARF usando OAuth2 e OpenID Connect. Cada sistema obtem tokens JWT que sao validados pela GEOAPI em cada requisicao.

Fluxo Authorization Code com PKCE e usado por aplicacoes com usuario interativo. REURBWEB e REURBMASTER redirecionam para Keycloak, usuario autentica, e retorna com authorization code trocado por tokens. REURBCAD usa custom URL scheme para capturar callback. GEOGIS usa servidor HTTP local temporario no desktop e exige autenticacao em duas etapas: apos login via Keycloak, o Analista informa uma AUTHENTICATION KEY (chave adicional que vincula sessao do plugin ao backend e habilita acesso as ortofotos do tenant).

## Tokens

Access token JWT de curta duracao (5 minutos) contem claims de identidade, roles e tenant_id. SSO session idle de 30 minutos e max de 10 horas para clients web. REURBCAD mobile usa scope offline_access com refresh token de 30 dias idle para operacao em campo sem internet. ID token fornece informacoes de perfil do usuario para exibicao na interface.
