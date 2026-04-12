---
type: leaf
status: review
updated: 2026-02-07
---

# PKCE Implementation - Seguranca e Erros

Tratamento de erros e consideracoes de seguranca da implementacao PKCE. Arquivo relacionado com 21a-pkce-overview.md e 21b-pkce-flows.md.

## Tratamento de Erros

| Erro | Causa | Acao | Log |
|------|-------|------|-----|
| state_mismatch | CSRF attack ou cookie expirado | Redirect para /auth/login com mensagem | Warning, potential CSRF attempt |
| code_expired | Usuario demorou para autorizar | Redirect para /auth/login, mensagem Sessao expirada | Info |
| invalid_grant | Code ja usado ou verifier incorreto | Redirect para /auth/login, mensagem Erro de autenticacao | Warning |
| cookie_missing | Cookie deletado ou third-party cookies bloqueados | Redirect para /auth/login, mensagem Cookies necessarios | Info |

## Consideracoes de Seguranca

PKCE protection previne code interception attacks garantindo que apenas quem gerou o verifier pode trocar o code por tokens. State protection previne CSRF attacks usando nonce aleatorio verificado no callback. Cookies httpOnly previnem acesso XSS ao verifier e tokens. Short lived state minimiza janela de ataque com cookie expirando em 10 minutos. One-time use garante que state e verifier sao usados apenas uma vez.

## Praticas Obrigatorias

Nunca armazenar code_verifier em localStorage pois e acessivel via JavaScript e vulneravel a XSS. Sempre usar method S256 e nunca plain pois plain nao protege contra interceptacao. Nunca reutilizar state ou verifier entre fluxos de autenticacao. Nunca aceitar state sem validacao contra o valor salvo no cookie.
