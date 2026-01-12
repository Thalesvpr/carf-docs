# SyncLog

Entidade representando registro operação sincronização offline app mobile REURBCAD com servidor GEOAPI rastreando cada CREATE/UPDATE/DELETE enviado dispositivo com detecção automática conflitos via versionamento otimista. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem TenantId Guid FK isolando logs cliente, AccountId Guid FK Account usuário sincronizou, DeviceId string identificador dispositivo, Direction string UPLOAD/DOWNLOAD sentido sync, EntityType tipo entidade (UNIT HOLDER COMMUNITY) e Operation string CREATE/UPDATE/DELETE.

Campos versionamento incluem BaseVersion byte array RowVersion dispositivo tinha enviar crucial detecção conflito, SyncStatus (PENDING SUCCESS CONFLICT FAILED), Payload JSON dados operação completa, ErrorMessage string nullable se FAILED, ConflictData JSON nullable dados conflitantes versão servidor vs dispositivo e SyncedAt DateTime timestamp.

Métodos incluem DetectConflict() comparando BaseVersion RowVersion atual retornando true se diferentes outro cliente modificou, ResolveConflict(mergeStrategy) aplicando AUTO campos distintos ou MANUAL escolha usuário, Retry() reenviando FAILED após correção e MarkAsSuccess()/MarkAsFailed(reason). Dispara SyncConflictEvent detectando conflito notificando técnico campo app, SyncCompletedEvent sucesso e integra WatermelonDB mobile mantendo fila operações pendentes até conectividade retornar.

---

**Última atualização:** 2026-01-12
