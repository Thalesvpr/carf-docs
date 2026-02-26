---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-175: Status de Processo

## Descricao

Sistema deve implementar workflow estruturado de tramitacao de processos atraves de enum de status definindo estados possiveis: Em Analise para processos sob avaliacao tecnica inicial, Documentacao Pendente quando identificadas lacunas documentais, Aprovado para processos que atenderam requisitos tecnicos e juridicos, Concluido quando titulo foi emitido ao beneficiario, e Indeferido para processos que nao atenderam criterios de elegibilidade. Matriz de transicoes validas estabelece mudancas de status permitidas conforme logica de negocio, prevenindo transicoes inconsistentes. Todas as mudancas registradas em log historico com data/hora, usuario responsavel, status de origem e destino, alem de justificativa textual obrigatoria documentando motivacao da transicao.

## Criterios de Aceitacao

1. Enum com status Em Analise, Pendente, Aprovado, Concluido, Indeferido
2. Matriz de transicoes validas
3. Bloqueio de transicoes invalidas
4. Log de transicao com justificativa obrigatoria
5. Historico completo de tramitacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-172
