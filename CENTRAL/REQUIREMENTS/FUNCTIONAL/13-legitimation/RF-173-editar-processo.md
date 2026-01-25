---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-173: Editar Processo

## Descricao

Sistema deve permitir atualizacao de dados cadastrais do processo de legitimacao fundiaria. Edicao inclui complementacao de informacoes do requerente, atualizacao de fundamentacao legal, correcao de dados protocolares e inclusao de observacoes tecnicas ou juridicas. Operacoes de edicao submetidas a validacao de permissoes baseada em roles e status do processo, garantindo que apenas usuarios autorizados modifiquem informacoes sensiveis e processos em estados Concluido ou Arquivado nao sejam alterados. Sistema registra log detalhado de alteracoes capturando timestamp, usuario responsavel, campos modificados com valores anteriores e novos, estabelecendo trilha de auditoria completa para conformidade com principios de gestao publica e accountability.

## Criterios de Aceitacao

1. Edicao de campos cadastrais permitidos
2. Validacao de permissoes por role
3. Bloqueio de edicao em status finais
4. Log de auditoria com valores anteriores e novos
5. Justificativa obrigatoria para alteracoes sensiveis

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-172
