---
type: readme
status: review
updated: 2026-01-12
---

# EVENTS

Domain events emitidos pelas entidades aggregate roots quando mudanças significativas ocorrem no domínio, processados de forma assíncrona após SaveChanges bem-sucedido para manter consistência transacional. Eventos core incluem UnitCreatedEvent, UnitUpdatedEvent, UnitDeletedEvent (soft delete), UnitStatusChangedEvent (transições de workflow), HolderLinkedEvent e HolderUnlinkedEvent (vínculos de titulares), UserLoggedInEvent, ApiKeyCreatedEvent, DocumentUploadedEvent, SyncCompletedEvent e SyncConflictEvent (sincronização mobile). Eventos de Teams gerenciam ciclo de vida de equipes (TeamCreatedEvent, TeamMemberAddedEvent, TeamMemberRemovedEvent, CommunityAuthorizationGrantedEvent, CommunityAuthorizationRevokedEvent). Eventos de Blocks/Plots rastreiam mudanças espaciais (BlockCreatedEvent, BlockUpdatedEvent, PlotCreatedEvent, PlotUpdatedEvent, UnitLinkedToPlotEvent). Eventos de GeoServices monitoram integrações WMS (WmsServerAddedEvent, WmsServerSyncedEvent, WmsLayerEnabledEvent). Eventos de Surveying acompanham topografia (SurveyPointCreatedEvent, SurveyPointProcessedEvent, SurveyPointApprovedEvent, MonographGeneratedEvent). Eventos de Legitimation controlam fluxo de certidões (LegitimationRequestCreatedEvent, LegitimationRequestAnalyzedEvent, LegitimationCertificateIssuedEvent, DescriptiveMemorialGeneratedEvent, LegitimationPlanGeneratedEvent). Eventos de Annotations gerenciam anotações (AnnotationCreatedEvent, AnnotationResolvedEvent, AnnotationDueEvent). Usos incluem notificações in-app/email/push, invalidação de cache, disparo de jobs em background e integração com sistemas externos.

## Arquivos

- **[00-i-domain-event.md](./00-i-domain-event.md)** - Interface base domain event marcador
- **[01-unit-created-event.md](./01-unit-created-event.md)** - Evento unidade criada disparado SaveChanges
- **[02-sync-conflict-event.md](./02-sync-conflict-event.md)** - Evento conflito sincronização mobile
- **[03-legitimation-certificate-issued-event.md](./03-legitimation-certificate-issued-event.md)** - Evento certidão legitimação emitida

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (22)

| Documento | Status |
|-----------|--------|
| [IDomainEvent](./00-i-domain-event.md) | ⚠ |
| [UnitCreatedEvent](./01-unit-created-event.md) | ⚠ |
| [HolderLinkedEvent](./02-holder-linked-event.md) | ⚠ |
| [SyncConflictEvent](./02-sync-conflict-event.md) | ⚠ |
| [HolderUnlinkedEvent](./03-holder-unlinked-event.md) | ⚠ |
| [LegitimationCertificateIssuedEvent](./03-legitimation-certificate-issued-event.md) | ⚠ |
| [UnitStatusChangedEvent](./04-unit-status-changed-event.md) | ⚠ |
| [DocumentUploadedEvent](./05-document-uploaded-event.md) | ⚠ |
| [CommunityCreatedEvent](./06-community-created-event.md) | ⚠ |
| [CommunityBoundaryChangedEvent](./07-community-boundary-changed-event.md) | ⚠ |
| [AccessGrantedEvent](./08-access-granted-event.md) | ⚠ |
| [AccessRevokedEvent](./09-access-revoked-event.md) | ⚠ |
| [BlockAddedEvent](./10-block-added-event.md) | ⚠ |
| [CommunityArchivedEvent](./11-community-archived-event.md) | ⚠ |
| [RequestSubmittedEvent](./12-request-submitted-event.md) | ⚠ |
| [ResponseAddedEvent](./13-response-added-event.md) | ⚠ |
| [RequestApprovedEvent](./14-request-approved-event.md) | ⚠ |
| [CertificateIssuedEvent](./15-certificate-issued-event.md) | ⚠ |
| [ContestationReceivedEvent](./16-contestation-received-event.md) | ⚠ |
| [DeadlineApproachingEvent](./17-deadline-approaching-event.md) | ⚠ |
| [RequestRejectedEvent](./18-request-rejected-event.md) | ⚠ |
| [CorrectionRequestedEvent](./19-correction-requested-event.md) | ⚠ |

<!-- CARF-INDEX-END -->
