# AUDIT

Entity auditoria compliance do GEOAPI registrando operações críticas sensíveis rastreabilidade accountability LGPD requisitos legais. AuditLog captura cada operação relevante com EntityType e EntityId identificando alvo, Operation enum (CREATE/UPDATE/DELETE/VIEW) incluindo reads sensitive data PII titular documentos, PerformedBy AccountId usuário responsável action permitindo rastreamento individual não repúdio, PerformedAt timestamp UTC precisão microsegundos ordenação cronológica exata, IpAddress e UserAgent contexto request detecção anomalias acessos suspeitos, OldValue JSON nullable snapshot antes mudança facilitando rollback auditoria forense, NewValue JSON snapshot após mudança permitindo reconstituir estado histórico qualquer momento através replay logs sequential, ChangeReason texto justificativa obrigatória operações críticas deletion titular aprovação legitimação atípica explicando decisão e IsSuccess boolean distinguindo tentativas falhadas bem-sucedidas registrando ambas detectar acessos não autorizados rejeitados. Logs imutáveis append-only sem updates deletes garantindo integridade evidência, armazenados PostgreSQL partitioned tables mensalmente otimizando queries recentes mantendo histórico completo archived S3 Glacier após retention period ativo conforme política retenção LGPD minimizando custos storage mantendo compliance legal cinco anos laudos periciais disputas judiciais requisições Ministério Público fiscalização órgãos controle.

## Arquivos

- **[32-audit-log.md](./32-audit-log.md)** - Log auditoria operações críticas compliance

---

**Última atualização:** 2026-01-12
