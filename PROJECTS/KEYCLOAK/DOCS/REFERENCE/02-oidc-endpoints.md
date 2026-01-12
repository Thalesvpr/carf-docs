# OpenID Connect Endpoints

OIDC endpoints do realm CARF seguindo especificação OpenID Connect Core 1.0 com discovery document em /.well-known/openid-configuration retornando todos endpoints e capabilities suportadas. Authorization endpoint /protocol/openid-connect/auth inicia fluxo OAuth2 recebendo response_type code, client_id, redirect_uri, scope openid profile email, state CSRF, code_challenge PKCE S256, retornando authorization code via redirect. Token endpoint /protocol/openid-connect/token troca code por tokens via POST form-urlencoded com grant_type authorization_code, code, redirect_uri, client_id, code_verifier PKCE, retornando JSON access_token refresh_token id_token expires_in. UserInfo endpoint /protocol/openid-connect/userinfo retorna claims usuário autenticado via GET com Bearer token. JWKS endpoint /protocol/openid-connect/certs retorna public keys RSA para validação JWT signature. Logout endpoint /protocol/openid-connect/logout encerra sessão SSO recebendo id_token_hint e post_logout_redirect_uri. Introspection /protocol/openid-connect/token/introspect valida token retornando active boolean e claims, requer client authentication. Revocation /protocol/openid-connect/revoke invalida refresh_token específico.

---

**Última atualização:** 2026-01-12
