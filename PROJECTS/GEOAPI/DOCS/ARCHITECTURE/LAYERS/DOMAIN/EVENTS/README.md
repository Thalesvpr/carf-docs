# EVENTS

Domain events emitidos pelas entidades aggregate roots quando mudanças significativas ocorrem no domínio, processados de forma assíncrona após SaveChanges bem-sucedido para manter consistência transacional. Eventos core incluem UnitCreatedEvent, UnitUpdatedEvent, UnitDeletedEvent (soft delete), UnitStatusChangedEvent (transições de workflow), HolderLinkedEvent e HolderUnlinkedEvent (vínculos de titulares), UserLoggedInEvent, ApiKeyCreatedEvent, DocumentUploadedEvent, SyncCompletedEvent e SyncConflictEvent (sincronização mobile). Eventos de Teams gerenciam ciclo de vida de equipes (TeamCreatedEvent, TeamMemberAddedEvent, TeamMemberRemovedEvent, CommunityAuthorizationGrantedEvent, CommunityAuthorizationRevokedEvent). Eventos de Blocks/Plots rastreiam mudanças espaciais (BlockCreatedEvent, BlockUpdatedEvent, PlotCreatedEvent, PlotUpdatedEvent, UnitLinkedToPlotEvent). Eventos de GeoServices monitoram integrações WMS (WmsServerAddedEvent, WmsServerSyncedEvent, WmsLayerEnabledEvent). Eventos de Surveying acompanham topografia (SurveyPointCreatedEvent, SurveyPointProcessedEvent, SurveyPointApprovedEvent, MonographGeneratedEvent). Eventos de Legitimation controlam fluxo de certidões (LegitimationRequestCreatedEvent, LegitimationRequestAnalyzedEvent, LegitimationCertificateIssuedEvent, DescriptiveMemorialGeneratedEvent, LegitimationPlanGeneratedEvent). Eventos de Annotations gerenciam anotações (AnnotationCreatedEvent, AnnotationResolvedEvent, AnnotationDueEvent). Usos incluem notificações in-app/email/push, invalidação de cache, disparo de jobs em background e integração com sistemas externos.

## Arquivos

- **[00-i-domain-event.md](./00-i-domain-event.md)** - Interface base domain event marcador
- **[01-unit-created-event.md](./01-unit-created-event.md)** - Evento unidade criada disparado SaveChanges
- **[02-sync-conflict-event.md](./02-sync-conflict-event.md)** - Evento conflito sincronização mobile
- **[03-legitimation-certificate-issued-event.md](./03-legitimation-certificate-issued-event.md)** - Evento certidão legitimação emitida

---

**Última atualização:** 2026-01-12
