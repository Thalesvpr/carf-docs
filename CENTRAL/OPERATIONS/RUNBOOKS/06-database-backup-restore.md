# Database Backup e Restore

Runbook para operações de backup e restore do PostgreSQL com dados geoespaciais PostGIS.

## Backup Manual

```bash
# Backup completo com compressão
pg_dump -h postgres -U carf -d carf -Fc -Z9 -f backup_$(date +%Y%m%d_%H%M%S).dump

# Backup apenas schema (sem dados)
pg_dump -h postgres -U carf -d carf --schema-only -f schema_backup.sql

# Backup de tabela específica
pg_dump -h postgres -U carf -d carf -t units -Fc -f units_backup.dump

# Backup com paralelismo (mais rápido)
pg_dump -h postgres -U carf -d carf -Fc -j 4 -f backup_parallel.dump
```

## Verificar Backup

```bash
# Listar conteúdo do backup
pg_restore -l backup.dump | head -50

# Verificar integridade
pg_restore --list backup.dump > /dev/null && echo "OK" || echo "CORRUPTED"

# Tamanho do backup
ls -lh backup.dump
```

## Restore Completo

```bash
# ATENÇÃO: Isso substitui o banco inteiro!

# 1. Desconectar usuários
psql -h postgres -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'carf' AND pid <> pg_backend_pid();"

# 2. Dropar e recriar banco
psql -h postgres -U postgres -c "DROP DATABASE IF EXISTS carf;"
psql -h postgres -U postgres -c "CREATE DATABASE carf OWNER carf;"

# 3. Restaurar extensões primeiro
psql -h postgres -U carf -d carf -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -h postgres -U carf -d carf -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"

# 4. Restore
pg_restore -h postgres -U carf -d carf -Fc -j 4 backup.dump
```

## Restore de Tabela Específica

```bash
# Extrair apenas uma tabela
pg_restore -h postgres -U carf -d carf -t units -Fc backup.dump

# Restore com dados apenas (sem schema)
pg_restore -h postgres -U carf -d carf -t units --data-only -Fc backup.dump
```

## Restore de Tenant Específico

```bash
# Exportar dados de um tenant
psql -h postgres -U carf -d carf -c "\COPY (SELECT * FROM units WHERE tenant_id = 'uuid-tenant') TO 'units_tenant.csv' CSV HEADER;"

# Importar em outro ambiente
psql -h postgres-dev -U carf -d carf -c "\COPY units FROM 'units_tenant.csv' CSV HEADER;"
```

## Backups Automatizados

Verificar CronJob no Kubernetes:
```bash
kubectl get cronjobs -n carf
kubectl describe cronjob pg-backup -n carf
kubectl logs job/pg-backup-xxxxx -n carf
```

## Política de Retenção

- Diários: 7 dias
- Semanais: 4 semanas
- Mensais: 12 meses
- Armazenamento: S3 Glacier após 30 dias

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
