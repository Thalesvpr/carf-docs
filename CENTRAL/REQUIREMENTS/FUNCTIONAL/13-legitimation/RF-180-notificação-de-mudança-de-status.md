---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-180: Notificacao de Mudanca de Status

## Descricao

Sistema deve implementar mecanismo automatizado de notificacao informando titular da unidade territorial sempre que processo de legitimacao sofrer transicao de status. Notificacoes enviadas atraves de multiplos canais incluindo email automatico para endereco cadastrado e notificacao in-app exibida na interface quando usuario autenticado. Templates personalizaveis estruturam conteudo das notificacoes conforme tipo de transicao, incluindo novo status, data da mudanca, proximos passos esperados e orientacoes sobre documentacao ou providencias necessarias. Administradores configuram quais transicoes disparam alertas, personalizam textos dos templates e definem regras de agrupamento evitando envio excessivo de mensagens.

## Criterios de Aceitacao

1. Notificacao por email automatico
2. Notificacao in-app para usuarios autenticados
3. Templates personalizaveis por tipo de transicao
4. Configuracao de transicoes que disparam alertas
5. Regras de agrupamento anti-spam

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-175
