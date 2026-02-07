---
type: leaf
status: approved
updated: 2026-02-07
---

# Legitimation Status Machine

Maquina de estados formal do processo de legitimacao fundiaria conforme Lei 13.465/2017. O processo possui 11 estados que refletem as etapas legais obrigatorias desde a submissao do requerimento ate o registro definitivo em cartorio. Prazos legais sao enforced pelo sistema via jobs agendados no Hangfire que disparam alertas quando deadlines se aproximam e executam transicoes automaticas quando prazos vencem.

## Tabela de Transicoes

| Estado Origem | Acao | Estado Destino | Roles | Prazo Legal | Evento | Detalhes |
|---------------|------|----------------|-------|-------------|--------|----------|
| DRAFT | submit | SUBMITTED | analyst | Sem prazo legal. | RequestSubmittedEvent | Requerimento deve ter unit_id valida com status APPROVED, ao menos um titular vinculado como PROPRIETARIO, e documentacao minima (foto fachada, documento identificacao do titular). |
| SUBMITTED | startAnalysis | UNDER_ANALYSIS | analyst | Sem prazo legal para inicio, mas SLA interno de 5 dias uteis. | AnalysisStartedEvent | Analyst assume responsabilidade. Campo analyst_id preenchido. |
| UNDER_ANALYSIS | publishNotification | NOTIFICATION_PUBLISHED | manager | Publicacao em diario oficial obrigatoria conforme Art. 25 da Lei. | NotificationPublishedEvent | Requer aprovacao do manager. Data de publicacao registrada em published_at. Inicia contagem do prazo de contestacao. |
| NOTIFICATION_PUBLISHED | startContestation | CONTESTATION_PERIOD | automatico | 30 dias corridos para terceiros contestarem, contados a partir da publicacao. | DeadlineApproachingEvent emitido 7 dias antes do vencimento. | Transicao automatica imediata apos publicacao. Campo contestation_deadline preenchido com data da publicacao mais 30 dias. |
| CONTESTATION_PERIOD | closeContestation | DECISION_PENDING | automatico apos vencimento do prazo | 120 dias para decisao final conforme regulamento. | ContestationClosedEvent | Job Hangfire verifica diariamente. Quando contestation_deadline vence sem contestacao, transiciona automaticamente. Campo deadline preenchido com 120 dias a partir do fechamento. |
| DECISION_PENDING | approve | APPROVED | manager | Dentro do prazo de 120 dias. | RequestApprovedEvent | Decisao registrada com decision APPROVED. Requer que nao haja contestacoes pendentes nao resolvidas. |
| DECISION_PENDING | reject | REJECTED | manager | Dentro do prazo de 120 dias. | RequestRejectedEvent | Justificativa obrigatoria em decision_reason com minimo de 100 caracteres citando fundamento legal. Decision REJECTED registrada com timestamp. |
| APPROVED | issueTitle | TITLE_ISSUED | manager | Emissao em ate 30 dias apos aprovacao. | CertificateIssuedEvent | Gera LegitimationCertificate com numero unico sequencial. PDF gerado automaticamente com dados do imovel, titular e fundamento legal. |
| TITLE_ISSUED | register | REGISTERED | admin | Registro no cartorio de imoveis. | RegistrationCompletedEvent | Estado terminal. Numero de matricula do cartorio registrado. Processo concluido. |
| Qualquer estado exceto REGISTERED e REJECTED | receiveContestation | CONTESTATION_RECEIVED | externo (protocolo administrativo) | Somente durante CONTESTATION_PERIOD, mas o sistema aceita registro em qualquer estado ativo para fins de documentacao. | ContestationReceivedEvent | Registra LegitimationResponse com response_type CONTESTATION. Inclui identificacao do contestante, fundamento e documentos. Suspende transicoes automaticas ate resolucao. |
| CONTESTATION_RECEIVED | resolveContestation | DECISION_PENDING | analyst, manager | Sem prazo legal especifico, mas prazo de 120 dias continua correndo. | ContestationResolvedEvent | Analyst analisa contestacao e registra parecer. Se contestacao improcedente, retorna a DECISION_PENDING. Se procedente, manager pode rejeitar o processo. |

## Prazos Legais

O prazo de contestacao de 30 dias e improrrogavel conforme Lei 13.465/2017. O sistema nao permite extensao desse prazo. Apos vencimento sem contestacao, a transicao para DECISION_PENDING e automatica e irreversivel.

O prazo de 120 dias para decisao final e monitorado por job Hangfire que emite DeadlineApproachingEvent aos 90, 100, 110 e 115 dias. Ultrapassar o prazo nao impede a decisao mas gera alerta ao admin do tenant.

## Estados Terminais

REGISTERED e REJECTED sao estados terminais. Nenhuma transicao e permitida a partir deles. Um processo rejeitado pode ser recriado como novo processo (novo DRAFT) referenciando o anterior, mas o registro original permanece inalterado para fins de auditoria.

## Auditoria

Cada transicao gera registro em audit_logs com estado anterior, novo estado, usuario responsavel e timestamp. Decisoes (approve/reject) incluem a justificativa completa no campo new_values do audit log. Contestacoes recebidas sao registradas como LegitimationResponse vinculadas ao request_id com todos os dados do contestante preservados.
