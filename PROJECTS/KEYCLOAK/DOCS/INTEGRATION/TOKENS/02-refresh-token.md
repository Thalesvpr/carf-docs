---
type: leaf
status: review
updated: 2026-01-19
---

# Refresh Token

Refresh token permite obter novo access token sem solicitar credenciais do usuário novamente. Tempo de vida idle de 30 minutos (ssoSessionIdleTimeout: 1800) e máximo absoluto de 10 horas (ssoSessionMaxLifespan: 36000). Com Remember Me ativo: idle 1 dia, max 7 dias. Refresh token rotation está atualmente DESLIGADA no realm-export.json (revokeRefreshToken: false, refreshTokenMaxReuse: 0) — ADR-003 recomenda ativar antes de ir para produção.

Frontend armazena refresh token em cookie HttpOnly com flags Secure e SameSite=Strict. Cookie inacessível via JavaScript protege contra XSS. Axios interceptor detecta resposta 401 do backend, executa refresh silencioso via POST /token com grant_type=refresh_token, e repete requisição original com novo access token.

Fluxo de refresh silencioso: access token expira, GEOAPI retorna 401 Unauthorized, interceptor Axios captura erro, executa POST para /token endpoint com refresh_token, Keycloak valida e emite novo par de tokens, interceptor atualiza tokens em memória e cookie, requisição original é repetida automaticamente.

Refresh token inválido (expirado, já usado, ou revogado) resulta em redirecionamento para tela de login. Usuário deve autenticar novamente com credenciais.

REURBCAD mantém refresh token criptografado em secure storage do dispositivo (Keychain iOS, Keystore Android) para suportar modo offline. Ao retornar online, app tenta refresh; se falhar por expiração, solicita reautenticação.
