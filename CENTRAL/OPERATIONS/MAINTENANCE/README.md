# MAINTENANCE

Procedimentos de manutenção do CARF.

## Backup

Backup incremental diário do PostgreSQL usando pg_dump às 2h da madrugada. Retenção de 30 dias local e S3 Glacier para long-term. Restore usa pg_restore testando em staging antes de produção.

## Database Maintenance

- VACUUM ANALYZE semanal aos domingos às 3h
- REINDEX trimestral se bloat maior que 30%
- Monitoring de slow queries via Kubernetes CronJob

## Checklist Manutenção

**Pré-manutenção:**
- Notificar usuários
- Ativar modo read-only
- Fazer backup fresh

**Pós-manutenção:**
- Executar smoke tests
- Verificar integridade dos dados
- Validar alertas de monitoring

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
