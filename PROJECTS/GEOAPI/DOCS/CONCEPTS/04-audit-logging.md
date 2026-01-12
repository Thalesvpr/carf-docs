# Audit Logging

Sistema de auditoria do GEOAPI captura TODAS operações de escrita (Commands) registrando quem via user_id do JWT, quando via timestamp UTC, o quê via tipo de comando e entity afetada, onde via tenant_id, e detalhes via JSON com valores antes/depois para updates. Dados armazenados em tabela audit_logs com colunas id timestamp user_id user_email tenant_id entity_type entity_id action (CREATE/UPDATE/DELETE) old_values new_values JSONB ip_address user_agent command_type, indexados para queries rápidas por entity user timestamp tenant.

Implementação via MediatR IPipelineBehavior AuditLoggingBehavior que intercepta todos Commands (ignorando Queries), captura snapshot antes da execução para UPDATE/DELETE, executa comando via next(), captura snapshot depois para CREATE/UPDATE, determina action baseado no nome do comando (Create* → CREATE, Update* → UPDATE, Delete* → DELETE), e salva AuditLog com todos os dados extraídos do request response CurrentUserService e HttpContext. Registrado no DI via AddBehavior garantindo que toda operação de escrita seja auditada automaticamente sem código manual em cada handler.

Consultas de auditoria via endpoint /api/audit-logs restrito a ADMIN/SUPER_ADMIN com filtros por entityType entityId userId startDate endDate suportando paginação, e endpoint /api/audit-logs/timeline/{entityType}/{entityId} retornando timeline de mudanças com diff mostrando campos alterados from/to para cada operação. Compliance LGPD garante logs retidos por 7 anos conforme Art. 16, logs anonimizados após solicitação via direito ao esquecimento Art. 18, acesso restrito apenas ADMIN e SUPER_ADMIN, e criptografia em repouso via PostgreSQL TDE. Retenção automática via job pg_cron mensalmente deletando logs com mais de 7 anos. Performance otimizada via particionamento por mês para tabelas grandes (>10M rows) e índices compostos em entity_type entity_id timestamp, user_id timestamp e tenant_id timestamp.

---

**Última atualização:** 2026-01-12
