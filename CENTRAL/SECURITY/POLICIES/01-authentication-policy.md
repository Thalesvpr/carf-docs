---
type: leaf
status: rejected
description: "Duplicacao com ADR-029 e PROJECTS/KEYCLOAK. Consolidar em um lugar. Stub de 9 linhas - incompleto."
updated: 2026-01-19
---

# Authentication Policy

Política de autenticação do CARF via Keycloak SSO garantindo identidade verificada e sessões seguras. Autenticação obrigatória para todas operações exceto endpoints públicos documentação, healthcheck, e login, implementada via OAuth2/OIDC Authorization Code Flow com PKCE (Proof Key for Code Exchange) protegendo contra interceptação código autorização, tokens JWT assinados RS256 (RSA 2048-bit) validados em cada request verificando signature, expiration, issuer, e audience. Password policy exige mínimo 12 caracteres com uppercase, lowercase, números, e símbolos, proibindo senhas comuns (password123, admin, qwerty), expirando a cada 90 dias forçando renovação, e bloqueando conta após 5 tentativas falhas consecutivas desbloqueando apenas via email recovery ou admin manual. Multi-factor authentication (MFA) obrigatório para roles ADMIN e FISCAL usando TOTP (Google Authenticator, Authy) ou SMS backup, opcional mas recomendado para ANALYST e FIELD_AGENT, e bypass temporário permitido em emergências com aprovação dois admins e auditoria registrada. Session management limita sessões simultâneas (max 3 devices por usuário), inatividade 30min expira sessão forçando re-login, logout invalida refresh token servidor-side impedindo reuso, e revogação global possível (admin pode forçar logout todos usuários tenant em caso comprometimento).
