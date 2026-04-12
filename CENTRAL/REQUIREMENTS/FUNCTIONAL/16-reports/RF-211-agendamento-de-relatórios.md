---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-211: Agendamento de Relatorios

## Descricao

Sistema deve oferecer funcionalidade de agendamento que permite configurar geracao e distribuicao automatica de relatorios em intervalos regulares, eliminando necessidade de solicitacoes manuais recorrentes. Interface de agendamento permite definir periodicidade (diaria, semanal, mensal) especificando dia da semana ou mes preferencial. Cada agendamento inclui tipo de relatorio, filtros e parametros aplicaveis, lista de destinatarios para envio por email, e assunto/corpo personalizados. Gerenciamento centralizado lista agendamentos ativos, permite edicao, desativacao ou exclusao, e exibe historico de execucoes incluindo datas de geracao e eventuais falhas, proporcionando transparencia e controle sobre automacoes.

## Criterios de Aceitacao

1. Periodicidade diaria, semanal, mensal
2. Configuracao de tipo e filtros
3. Lista de destinatarios por email
4. Historico de execucoes
5. Gerenciamento centralizado de agendamentos

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-203, RF-207
