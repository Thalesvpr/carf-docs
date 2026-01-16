# Backup Procedures

Procedimentos de backup do PostgreSQL com PostGIS para garantir recuperação de dados em caso de falhas.

## Backup Diário Automatizado

CronJob Kubernetes executa às 02:00 UTC:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: pg-backup-daily
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: pg-backup
            image: postgres:16
            command:
            - /bin/sh
            - -c
            - |
              BACKUP_FILE="carf_$(date +%Y%m%d_%H%M%S).dump"
              pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -Fc -Z9 -f /backups/$BACKUP_FILE
              aws s3 cp /backups/$BACKUP_FILE s3://carf-backups/daily/$BACKUP_FILE
            envFrom:
            - secretRef:
                name: pg-credentials
```

## Verificação de Integridade

```bash
# Verificar backup mais recente
aws s3 ls s3://carf-backups/daily/ --recursive | sort | tail -1

# Download e teste de restore em ambiente isolado
aws s3 cp s3://carf-backups/daily/carf_20260116.dump /tmp/
pg_restore -l /tmp/carf_20260116.dump > /dev/null && echo "Backup válido"

# Teste de restore completo (em staging)
createdb carf_restore_test
pg_restore -d carf_restore_test /tmp/carf_20260116.dump
psql -d carf_restore_test -c "SELECT count(*) FROM units;"
dropdb carf_restore_test
```

## Política de Retenção

| Tipo | Frequência | Retenção | Storage |
|------|------------|----------|---------|
| Diário | 02:00 UTC | 7 dias | S3 Standard |
| Semanal | Domingo 03:00 | 4 semanas | S3 Standard |
| Mensal | Dia 1, 04:00 | 12 meses | S3 Glacier |
| Anual | Jan 1, 05:00 | 7 anos | S3 Glacier Deep |

## Lifecycle Policy S3

```json
{
  "Rules": [
    {
      "ID": "DailyBackupRetention",
      "Prefix": "daily/",
      "Status": "Enabled",
      "Expiration": {"Days": 7}
    },
    {
      "ID": "MonthlyToGlacier",
      "Prefix": "monthly/",
      "Status": "Enabled",
      "Transitions": [
        {"Days": 30, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }
  ]
}
```

## Monitoramento

Alertas configurados:
- Backup não executado há mais de 26 horas
- Tamanho do backup diminuiu mais de 10% (possível perda de dados)
- Falha no upload para S3

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
