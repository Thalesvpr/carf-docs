# SYNC

Entity gerenciamento sincronização offline mobile do GEOAPI rastreando operações realizadas campo sem conectividade detectando conflitos durante reconciliação servidor. SyncLog registra cada operação mobile com EntityType e EntityId identificando alvo, Operation enum (CREATE/UPDATE/DELETE) especificando mudança, LocalVersion timestamp device quando executada, ServerVersion nullable timestamp após sincronização bem-sucedida servidor, Payload JSON snapshot completo entity estado após operação permitindo aplicar change servidor mesmo entity tendo sido modificada entretanto, ConflictDetected boolean indicando ServerVersion entity atual difere BaseVersion esperada mobile sugerindo concurrent modification, ConflictResolution enum nullable (ACCEPT_LOCAL/ACCEPT_SERVER/MERGE_MANUAL) estratégia escolhida resolver e SyncStatus enum (PENDING/IN_PROGRESS/COMPLETED/FAILED/CONFLICT_REQUIRING_RESOLUTION) workflow sincronização. Estratégia detecção conflito compara BaseVersion mobile (último ServerVersion conhecido) contra ServerVersion atual entity servidor, se diferem significa outra modificação ocorreu entre fetch mobile e sync requirindo decisão merge geralmente ACCEPT_SERVER preservando última alteração servidor mas oferecendo ACCEPT_LOCAL forçar overwrite quando field agent tem informação mais recente validada presencialmente ou MERGE_MANUAL quando ambas mudanças devem ser preservadas seletivamente campo a campo via UI resolução conflitos apresentando diffs lado a lado.

## Arquivos

- **[15-sync-log.md](./15-sync-log.md)** - Log sincronização mobile detecção conflitos

---

**Última atualização:** 2026-01-12
