# Fluxos OAuth2 e OpenID Connect

Fluxo Authorization Code com PKCE é utilizado por aplicações frontend GEOWEB, REURBCAD, WEBDOCS e ADMIN sendo recomendado para SPAs e mobile por não requerer client_secret exposto no código cliente. Aplicação gera code_verifier random de 43-128 caracteres, calcula code_challenge como SHA256 do code_verifier em base64url encoding, redireciona usuário para endpoint de autorização Keycloak incluindo code_challenge e code_challenge_method S256. Após login bem-sucedido Keycloak retorna authorization code para redirect_uri da aplicação, aplicação troca code por tokens enviando code_verifier original que Keycloak valida contra code_challenge armazenado prevenindo authorization code interception attacks.

Fluxo Client Credentials é utilizado por GEOGIS plugin QGIS para autenticação server-to-server sem contexto de usuário humano. Plugin configurado como confidential client executa POST direto para token endpoint enviando client_id, client_secret e grant_type client_credentials. Keycloak retorna access_token contendo roles do service account sem claims de usuário, usado para autenticar requisições WFS/WMS para GEOAPI.

Bearer Token Validation no backend GEOAPI implementada via middleware ASP.NET Core que extrai JWT do header Authorization, valida assinatura usando public keys do JWKS endpoint com cache de 24 horas, verifica claims obrigatórios exp iss aud nbf, e popula HttpContext.User com ClaimsPrincipal contendo todos claims do token. Controllers acessam claims via User.FindFirst ou attributes [Authorize(Roles = "analyst")].

Refresh Token Strategy configurada com max reuse zero garantindo uso único onde cada refresh gera novo access_token e novo refresh_token invalidando anterior prevenindo replay attacks. Access token dura 5 minutos forçando refresh frequente reduzindo janela de exposição, refresh token dura conforme sessão SSO até 30 dias permitindo sessões persistentes.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
