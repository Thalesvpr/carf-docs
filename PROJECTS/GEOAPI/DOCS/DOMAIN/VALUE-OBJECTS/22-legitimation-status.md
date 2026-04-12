---
type: leaf
status: review
updated: 2026-02-08
---

# LegitimationStatus

Value object enum imutavel representando o estado atual de um processo de legitimacao fundiaria. Persiste na coluna status varchar(30) da tabela legitimation_requests com CHECK constraint. Workflow de 11 estados conforme Lei 13.465/2017.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| DRAFT | Rascunho. Processo criado mas nao protocolado. |
| SUBMITTED | Protocolado. Inicia contagem de prazos. |
| UNDER_ANALYSIS | Em analise por analista designado. |
| NOTIFICATION_PUBLISHED | Edital de notificacao publicado. |
| CONTESTATION_PERIOD | Periodo de 30 dias para contestacoes de terceiros. |
| CONTESTATION_RECEIVED | Contestacao recebida, aguardando analise. |
| DECISION_PENDING | Todas analises concluidas, aguardando decisao final do gestor. |
| APPROVED | Aprovado. Permite emissao de certidao. |
| REJECTED | Rejeitado com justificativa. |
| TITLE_ISSUED | Certidao de legitimacao emitida (LegitimationCertificate). |
| REGISTERED | Registrado em cartorio. Processo concluido. |

## Transicoes Validas

| De | Para | Condicao |
|----|------|----------|
| DRAFT | SUBMITTED | Documentacao minima preenchida. |
| SUBMITTED | UNDER_ANALYSIS | Analista designado assumiu processo. |
| UNDER_ANALYSIS | NOTIFICATION_PUBLISHED | Parecer tecnico favoravel, edital gerado. |
| NOTIFICATION_PUBLISHED | CONTESTATION_PERIOD | Automatico apos publicacao. |
| CONTESTATION_PERIOD | DECISION_PENDING | Prazo de 30 dias encerrado sem contestacao. |
| CONTESTATION_PERIOD | CONTESTATION_RECEIVED | Contestacao recebida durante prazo. |
| CONTESTATION_RECEIVED | DECISION_PENDING | Contestacao analisada e resolvida. |
| DECISION_PENDING | APPROVED | Decisao favoravel. |
| DECISION_PENDING | REJECTED | Decisao desfavoravel com justificativa obrigatoria. |
| APPROVED | TITLE_ISSUED | Certidao emitida. |
| TITLE_ISSUED | REGISTERED | Registro em cartorio confirmado. |

Prazo de 120 dias desde SUBMITTED nao pode ser ultrapassado sem justificativa formal registrada em Annotation.
