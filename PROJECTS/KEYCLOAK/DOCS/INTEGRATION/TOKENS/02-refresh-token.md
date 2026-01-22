---
type: leaf
status: review
updated: 2026-01-19
---

# Refresh Token

Refresh token permite obter novo access token sem solicitar credenciais do usuário novamente. Tempo de vida padrão de 30 minutos configurado em Realm Settings > Tokens > SSO Session Idle. Refresh token rotation ativado gera novo refresh token a cada uso invalidando o anterior.

Frontend armazena refresh token em cookie HttpOnly com flags Secure e SameSite=Strict. Cookie inacessível via JavaScript protege contra XSS. Axios interceptor detecta resposta 401 do backend, executa refresh silencioso via POST /token com grant_type=refresh_token, e repete requisição original com novo access token.

Fluxo de refresh silencioso: access token expira, GEOAPI retorna 401 Unauthorized, interceptor Axios captura erro, executa POST para /token endpoint com refresh_token, Keycloak valida e emite novo par de tokens, interceptor atualiza tokens em memória e cookie, requisição original é repetida automaticamente.

Refresh token inválido (expirado, já usado, ou revogado) resulta em redirecionamento para tela de login. Usuário deve autenticar novamente com credenciais.

REURBCAD mantém refresh token criptografado em secure storage do dispositivo (Keychain iOS, Keystore Android) para suportar modo offline. Ao retornar online, app tenta refresh; se falhar por expiração, solicita reautenticação.
