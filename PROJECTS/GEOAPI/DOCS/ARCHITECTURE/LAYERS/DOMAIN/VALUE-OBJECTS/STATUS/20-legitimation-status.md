---
type: leaf
status: review
updated: 2026-02-08
---

# LegitimationStatus

Value object enum representando o estado no workflow completo de processo de legitimacao fundiaria desde solicitacao inicial ate emissao de certidao final, conforme Lei 13.465/2017. No banco de dados, corresponde ao campo legitimation_requests.status (varchar(30)) com CHECK constraint.

O workflow possui 11 estados cobrindo toda a jornada legal, com transicoes rigorosas que garantem cumprimento dos prazos e requisitos normativos.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| DRAFT | Rascunho da solicitacao, editavel pelo requerente. |
| SUBMITTED | Submetido para analise inicial, protocolo gerado. |
| UNDER_ANALYSIS | Em analise tecnica pelo analista designado. |
| NOTIFICATION_PUBLISHED | Edital publicado aguardando prazo legal de contestacao. |
| CONTESTATION_PERIOD | Periodo aberto para contestacoes de terceiros (30 dias). |
| CONTESTATION_RECEIVED | Recebeu contestacao, requerendo analise juridica. |
| DECISION_PENDING | Aguardando decisao final do gestor. |
| APPROVED | Aprovado para emissao de certidao. |
| REJECTED | Rejeitado com justificativa, processo encerrado. |
| TITLE_ISSUED | Certidao de legitimacao emitida. |
| REGISTERED | Registrado em cartorio, processo concluido. |

## Transicoes Validas

| De | Para | Quem | Condicao |
| --- | --- | --- | --- |
| DRAFT | SUBMITTED | ANALYST, MANAGER | Documentacao minima preenchida. |
| SUBMITTED | UNDER_ANALYSIS | ANALYST | Analista designado assumiu processo. |
| UNDER_ANALYSIS | NOTIFICATION_PUBLISHED | ANALYST | Parecer tecnico favoravel, edital gerado. |
| NOTIFICATION_PUBLISHED | CONTESTATION_PERIOD | Sistema | Automatico apos publicacao do edital. |
| CONTESTATION_PERIOD | DECISION_PENDING | Sistema | Prazo de 30 dias encerrado sem contestacao. |
| CONTESTATION_PERIOD | CONTESTATION_RECEIVED | Sistema | Contestacao recebida durante prazo. |
| CONTESTATION_RECEIVED | DECISION_PENDING | MANAGER | Contestacao analisada e resolvida. |
| DECISION_PENDING | APPROVED | MANAGER | Decisao favoravel com justificativa. |
| DECISION_PENDING | REJECTED | MANAGER | Decisao desfavoravel com justificativa obrigatoria. |
| APPROVED | TITLE_ISSUED | MANAGER | Certidao emitida via IPdfGenerator. |
| TITLE_ISSUED | REGISTERED | REURBMASTER | Registro em cartorio confirmado. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| CanEdit() | bool | Verifica se permite alteracao (apenas DRAFT). |
| CanPublish() | bool | Verifica se pode publicar edital. |
| IsInLegalWaitingPeriod() | bool | Verifica se esta em prazo legal (CONTESTATION_PERIOD ou NOTIFICATION_PUBLISHED). |
| CanIssueCertificate() | bool | Verifica pre-requisitos para emissao (apenas APPROVED). |
| IsFinalState() | bool | Retorna true para REGISTERED e REJECTED. |
| GetNextPossibleStatuses() | list | Retorna transicoes validas a partir do estado atual. |
| ValidateTransition(LegitimationStatus) | void | Lanca ValidationException se transicao invalida. |

Usado em LegitimationRequest.Status controlando workflow com validacoes rigorosas de transicao, disparando eventos em cada mudanca e alimentando dashboards de acompanhamento do processo de regularizacao. Prazo de 120 dias desde SUBMITTED nao pode ser ultrapassado sem justificativa formal.
