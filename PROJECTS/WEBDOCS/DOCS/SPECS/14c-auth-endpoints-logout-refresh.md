---
type: leaf
status: review
updated: 2026-02-07
---

# Endpoints de Autenticacao - Logout e Refresh

Detalhamento de POST /auth/logout e POST /auth/refresh. Relacionado com 14a-auth-endpoints-overview.md.

## POST /auth/logout

Arquivo src/pages/auth/logout.ts. Limpa cookies carf_access_token e carf_refresh_token setando maxAge 0. Redireciona para Keycloak logout em /realms/REALM/protocol/openid-connect/logout com client_id e post_logout_redirect_uri. Resposta: 302 para Keycloak logout.

## POST /auth/refresh

Arquivo src/pages/api/refresh.ts. Le carf_refresh_token do cookie (401 se ausente). POST ao token endpoint como public client com grant_type refresh_token, client_id e refresh_token. Atualiza cookies com novos valores.

## Respostas do Refresh

| Cenario | Status | Corpo |
|---------|--------|-------|
| Sucesso | 200 | success true, expiresIn number |
| Sem refresh token | 401 | error no_refresh_token |
| Refresh expirado | 401 | error refresh_token_expired |
| Keycloak indisponivel | 502 | error keycloak_unavailable |

## JWT Payload

| Campo | Exemplo | Descricao |
|-------|---------|-----------|
| exp/iat | timestamps | Expiracao e emissao |
| iss | auth.carf.com.br/realms/carf | Emissor |
| sub | 1234567890 | ID do usuario |
| azp | carf-webdocs | Client solicitante |
| email | user@example.com | Email |
| name | Joao Silva | Nome completo |
| realm_access.roles | analyst, dev | Roles no realm |
| tenant_id | tenant-123 | Tenant do usuario |
