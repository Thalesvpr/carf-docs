---
id: UC-005-FE-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-005-FE-003: Token Expirado

Fluxo de excecao do UC-005 quando token de autenticacao expira durante sincronizacao.

## Condicao

Em qualquer fase do UC-005, servidor retorna erro de autenticacao por token expirado.

## Fluxo

1. Servidor detecta token expirado
2. Servidor retorna erro de autenticacao
3. App tenta renovar token automaticamente usando refresh token
4. Se renovacao sucede, app retoma sincronizacao
5. Se renovacao falha, app exibe tela de login

## Renovacao Automatica

- App usa refresh token armazenado
- Servidor emite novo par de tokens
- App retoma operacao transparentemente

## Falha de Renovacao

- Refresh token tambem expirado
- Usuario redirecionado para login
- Dados pendentes preservados localmente

## Retorno

Se refresh sucede, sincronizacao continua. Se falha, usuario faz login e retoma.

## Pos-condicoes

- Tokens renovados ou usuario re-autenticado
- Dados pendentes preservados em caso de re-login
