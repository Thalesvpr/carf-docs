---
type: leaf
status: review
updated: 2026-02-08
---

# Audit Logging

O sistema de auditoria da GEOAPI captura todas as operacoes de escrita registrando quem executou, quando, o que foi alterado e de onde, garantindo compliance com LGPD e rastreabilidade completa.

## Captura Automatica

A implementacao utiliza MediatR IPipelineBehavior (AuditLoggingBehavior) que intercepta todos os Commands automaticamente, ignorando Queries. Para UPDATE e DELETE, o behavior captura snapshot dos valores anteriores antes da execucao. Apos execucao bem-sucedida, captura valores posteriores para CREATE e UPDATE. Dados do usuario, tenant, IP e User-Agent sao extraidos do contexto HTTP.

## Tabela audit_logs

Os registros sao armazenados na tabela audit_logs com colunas id, tenant_id, user_id, action (CREATE, UPDATE, DELETE, LOGIN, LOGOUT, STATUS_CHANGE), entity_type, entity_id, old_values (JSONB com valores anteriores, null em CREATE), new_values (JSONB com novos valores, null em DELETE), ip_address e timestamp. A tabela e append-only: registros nunca sao atualizados ou deletados.

## Retencao e Performance

A retencao minima e de 7 anos conforme Art. 16 da LGPD para dados pessoais. Particionamento mensal e recomendado para tabelas com alto volume (acima de 10 milhoes de linhas). Indices compostos em (tenant_id, entity_type, entity_id) para historico de entidade, (tenant_id, user_id, timestamp) para auditoria por usuario e (tenant_id, timestamp) para consultas por periodo otimizam queries. Job pg_cron mensal deleta particoes com mais de 7 anos.

## Consulta

Endpoints /api/admin/audit-logs restritos a admin e super-admin permitem filtros por entityType, entityId, userId, startDate e endDate com paginacao padrao. A timeline de uma entidade mostra diff de campos alterados em cada operacao.

## LGPD Compliance

Logs sao anonimizados apos solicitacao via direito ao esquecimento (Art. 18 LGPD), substituindo dados pessoais por hash. Acesso restrito a roles admin e super-admin. Criptografia em repouso via PostgreSQL TDE protege dados armazenados.
