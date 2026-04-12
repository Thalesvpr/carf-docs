---
type: leaf
status: approved
updated: 2026-02-07
---

# LegitimationRequest

Entidade aggregate root representando processo de legitimacao fundiaria conforme Lei 13.465/2017. Coordena todo o ciclo de vida desde a submissao do requerimento ate a emissao de certidao e registro em cartorio, passando por analise tecnica, publicacao de edital, periodo de contestacao e decisao final. Herda de BaseAggregateRoot suportando domain events ao longo de cada transicao.

## Papel no Dominio

O LegitimationRequest formaliza o processo legal de regularizacao fundiaria de uma unidade. Sua maquina de estados com 11 estados (documentada em CENTRAL/DOMAIN-RULES/WORKFLOWS/05-legitimation-status-machine.md) reflete as etapas legais obrigatorias da Lei 13.465/2017, incluindo prazos improrrogaveis para contestacao (30 dias) e decisao (120 dias) monitorados via jobs Hangfire.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| UnitId | Guid | nao | FK para Unit. Unidade objeto da legitimacao. |
| Status | string | nao | Status atual. 11 valores: DRAFT, SUBMITTED, UNDER_ANALYSIS, NOTIFICATION_PUBLISHED, CONTESTATION_PERIOD, CONTESTATION_RECEIVED, DECISION_PENDING, APPROVED, REJECTED, TITLE_ISSUED, REGISTERED. |
| RequestedAt | DateTime | nao | Data de protocolo do requerimento. |
| RequestedBy | Guid | nao | Account que iniciou o processo. |
| AnalystId | Guid | sim | Analyst responsavel pela analise tecnica. Preenchido ao atribuir. |
| ManagerId | Guid | sim | Manager responsavel pela decisao. Preenchido ao decidir. |
| Decision | string | sim | APPROVED ou REJECTED. Preenchido na decisao final. |
| DecisionReason | string | sim | Justificativa da decisao com fundamento legal. Obrigatoria em rejeicao com minimo de 100 caracteres. |
| DecisionAt | DateTime | sim | Quando a decisao foi tomada. |
| Deadline | date | sim | Prazo para decisao final. 120 dias apos fechamento do periodo de contestacao. |
| ContestationDeadline | date | sim | Prazo final para contestacoes. 30 dias apos publicacao do edital. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Vinculado a uma Unit (obrigatorio) que e o objeto da legitimacao. Colecao de LegitimationResponses contendo pareceres tecnicos, decisoes e contestacoes. LegitimationCertificate gerado apos aprovacao.

## Invariantes de Negocio

Apenas uma LegitimationRequest ativa por Unit (constraint parcial excluindo REJECTED). Unit deve ter status APPROVED antes de iniciar processo. Ao menos um titular PROPRIETARIO deve estar vinculado a unidade. Prazo de contestacao de 30 dias e improrrogavel. REGISTERED e REJECTED sao estados terminais.

## Domain Events

RequestSubmittedEvent ao submeter. NotificationPublishedEvent ao publicar edital. DeadlineApproachingEvent quando prazos se aproximam. RequestApprovedEvent ao aprovar. RequestRejectedEvent ao rejeitar. CertificateIssuedEvent ao emitir certidao. ContestationReceivedEvent ao receber contestacao.
