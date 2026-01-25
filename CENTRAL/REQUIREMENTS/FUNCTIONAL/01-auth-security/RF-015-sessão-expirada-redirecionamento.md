---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
---

# RF-015: Sessao Expirada - Redirecionamento

## Descricao

Sistema deve detectar quando sessao expirou e renovacao via refresh_token falhou. Mensagem clara deve informar usuario que sessao expirou por inatividade, solicitando novo login. Funcionalidade de retorno a tela original apos re-login preserva contexto do usuario, permitindo continuar trabalho de onde parou.

## Criterios de Aceitacao

1. Deteccao automatica de sessao expirada
2. Mensagem amigavel explicando expiracao
3. Redirecionamento para login preservando URL original
4. Retorno a tela original apos re-autenticacao
5. Deep links e query parameters preservados

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD
- Requisitos dependentes: RF-004, RF-014
