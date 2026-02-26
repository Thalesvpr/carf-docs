---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - REURBCAD
---

# RF-002: Fluxo Authorization Code PKCE

## Descricao

Aplicacoes web REURBWEB e REURBCAD devem utilizar fluxo OAuth2 Authorization Code com extensao PKCE para autenticacao de usuarios. Cliente gera code_verifier aleatorio e envia code_challenge via SHA-256 durante solicitacao. Apos autenticacao no Keycloak, sistema redireciona com codigo temporario que cliente troca por tokens enviando code_verifier original. Tokens armazenados de forma segura usando httpOnly cookies para refresh_token.

## Criterios de Aceitacao

1. Fluxo PKCE implementado com code_verifier e code_challenge
2. Redirect URI validado contra lista registrada
3. Access token armazenado em memoria ou sessionStorage
4. Refresh token armazenado em httpOnly cookie
5. Protecao contra XSS e CSRF implementada

## Rastreabilidade

- Modulos: REURBWEB, REURBCAD
- Requisitos dependentes: RF-001, RF-004
