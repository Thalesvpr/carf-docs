---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - REURBCAD
---

# RF-014: Logout e Revogacao de Token

## Descricao

Usuario deve poder fazer logout voluntario do sistema revogando tokens ativos. Processo de logout remove tokens do storage local do cliente e opcionalmente chama endpoint de revogacao do Keycloak para invalidar tokens no servidor. Apos logout, usuario e redirecionado para tela de login com mensagem de confirmacao.

## Criterios de Aceitacao

1. Botao de logout visivel em interface de usuario
2. Tokens removidos do storage local apos logout
3. Redirecionamento para tela de login apos logout
4. Revogacao no servidor Keycloak opcional mas recomendada
5. Mensagem de confirmacao exibida ao usuario

## Rastreabilidade

- Modulos: REURBWEB, REURBCAD
- Requisitos dependentes: RF-001, RF-002
