# Storage Quota Exceeded

Runbook para resolver problemas de cota de armazenamento excedida em S3/MinIO para documentos e arquivos do CARF.

## Diagnóstico

```bash
# Verificar uso total do bucket
aws s3 ls s3://carf-documents --recursive --summarize --endpoint-url=$MINIO_ENDPOINT | tail -2

# Uso por tenant (prefixo)
aws s3 ls s3://carf-documents/tenants/ --endpoint-url=$MINIO_ENDPOINT | head -20

# Arquivos grandes (> 50MB)
aws s3 ls s3://carf-documents --recursive --endpoint-url=$MINIO_ENDPOINT | awk '$3 > 52428800 {print $0}'

# Arquivos antigos (verificar data)
aws s3 ls s3://carf-documents --recursive --endpoint-url=$MINIO_ENDPOINT | sort -k1,2 | head -50
```

## Verificar Quota por Tenant

```sql
-- Uso de storage por tenant
SELECT tenant_id,
       count(*) as total_files,
       pg_size_pretty(sum(file_size)) as total_size
FROM documents
GROUP BY tenant_id
ORDER BY sum(file_size) DESC;

-- Arquivos maiores por tenant
SELECT tenant_id, file_name, pg_size_pretty(file_size) as size, created_at
FROM documents
WHERE file_size > 10485760  -- > 10MB
ORDER BY file_size DESC
LIMIT 20;
```

## Limpeza de Arquivos

```bash
# Listar arquivos temporários órfãos
aws s3 ls s3://carf-documents/temp/ --recursive --endpoint-url=$MINIO_ENDPOINT

# Deletar temporários mais antigos que 7 dias
aws s3 ls s3://carf-documents/temp/ --recursive --endpoint-url=$MINIO_ENDPOINT | \
  awk -v date="$(date -d '7 days ago' +%Y-%m-%d)" '$1 < date {print $4}' | \
  xargs -I {} aws s3 rm s3://carf-documents/{} --endpoint-url=$MINIO_ENDPOINT

# Deletar versões antigas (se versionamento habilitado)
aws s3api list-object-versions --bucket carf-documents --endpoint-url=$MINIO_ENDPOINT | \
  jq '.DeleteMarkers[] | select(.IsLatest == false)' | head -20
```

## Lifecycle Policies

```bash
# Verificar lifecycle rules
aws s3api get-bucket-lifecycle-configuration --bucket carf-documents --endpoint-url=$MINIO_ENDPOINT

# Exemplo de policy para mover para Glacier após 90 dias
cat > lifecycle.json << 'EOF'
{
  "Rules": [
    {
      "ID": "MoveToGlacier",
      "Filter": {"Prefix": "archives/"},
      "Status": "Enabled",
      "Transitions": [
        {"Days": 90, "StorageClass": "GLACIER"}
      ]
    },
    {
      "ID": "DeleteTempFiles",
      "Filter": {"Prefix": "temp/"},
      "Status": "Enabled",
      "Expiration": {"Days": 7}
    }
  ]
}
EOF

aws s3api put-bucket-lifecycle-configuration --bucket carf-documents --lifecycle-configuration file://lifecycle.json --endpoint-url=$MINIO_ENDPOINT
```

## Expandir Quota

```bash
# MinIO: aumentar quota de tenant
mc admin quota set myminio/carf-documents --size 100GB

# Verificar quota atual
mc admin quota info myminio/carf-documents
```

## Notificação para Tenant

Quando tenant atinge 80% da quota, sistema deve:
1. Enviar email ao admin do tenant
2. Bloquear uploads quando atingir 100%
3. Mostrar alerta no dashboard

Query para verificar tenants próximos do limite:
```sql
SELECT t.name, t.storage_quota_gb,
       round(sum(d.file_size) / 1073741824.0, 2) as used_gb,
       round(sum(d.file_size) / (t.storage_quota_gb * 1073741824.0) * 100, 1) as percent_used
FROM tenants t
JOIN documents d ON d.tenant_id = t.id
GROUP BY t.id
HAVING sum(d.file_size) > t.storage_quota_gb * 1073741824.0 * 0.8
ORDER BY percent_used DESC;
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
