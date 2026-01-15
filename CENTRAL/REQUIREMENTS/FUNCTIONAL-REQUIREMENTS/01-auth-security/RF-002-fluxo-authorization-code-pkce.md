---
modules: [GEOWEB]
epic: security
---

# RF-002: Fluxo Authorization Code + PKCE

Aplicações web GEOWEB e REURBCAD devem utilizar fluxo OAuth2 Authorization Code com extensão PKCE (Proof Key for Code Exchange) garantindo segurança adicional contra ataques de interceptação de código de autorização onde cliente gera code_verifier aleatório e envia code_challenge derivado via SHA-256 durante solicitação inicial de autorização, após usuário autenticar no Keycloak sistema redireciona de volta para aplicação com código de autorização temporário que cliente troca por access_token enviando code_verifier original permitindo servidor Keycloak validar autenticidade da requisição, redirecionamento seguro após login implementado com validação de redirect_uri registrado previamente evitando ataques de redirecionamento aberto, tokens (access_token refresh_token) devem ser armazenados de forma segura no cliente utilizando mecanismos como httpOnly cookies para refresh_token e sessionStorage ou memória para access_token evitando exposição via JavaScript e XSS, implementação garante conformidade com melhores práticas OAuth2 para aplicações públicas SPA (Single Page Applications).

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
