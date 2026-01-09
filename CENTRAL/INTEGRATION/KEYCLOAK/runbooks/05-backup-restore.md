# Backup e Restore

## Backup Automático

### Executar backup
```bash
cd PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak
make backup
```

### Agenda automática (cron)
```bash
# Backup diário às 2am
0 2 * * * cd /path/to/carf-keycloak && make backup

# Backup semanal com limpeza de backups antigos
0 3 * * 0 cd /path/to/carf-keycloak && make backup && find backups/ -mtime +30 -delete
```

## Backup Manual

### PostgreSQL
```bash
docker exec carf-keycloak-postgres-dev pg_dump -U keycloak keycloak > backup.sql
```

### Realm export
```bash
docker exec carf-keycloak-dev /opt/keycloak/bin/kc.sh export \
  --realm carf \
  --file /tmp/realm.json \
  --users realm_file

docker cp carf-keycloak-dev:/tmp/realm.json ./realm-backup.json
```

## Restore

### Via script
```bash
# Listar backups disponíveis
ls -lh backups/

# Restore do backup mais recente
make restore FILE=backups/keycloak_backup_20260109_143000.tar.gz
```

### Manual

#### 1. Parar Keycloak
```bash
docker-compose -f docker-compose.dev.yml stop keycloak
```

#### 2. Restore PostgreSQL
```bash
# Drop e recriar database
docker exec -it carf-keycloak-postgres-dev psql -U keycloak -c "DROP DATABASE keycloak;"
docker exec -it carf-keycloak-postgres-dev psql -U keycloak -c "CREATE DATABASE keycloak;"

# Restore dump
docker exec -i carf-keycloak-postgres-dev psql -U keycloak keycloak < backup.sql
```

#### 3. Restart Keycloak
```bash
docker-compose -f docker-compose.dev.yml start keycloak
```

## Disaster Recovery

### Cenário: Perda total do servidor

#### 1. Novo servidor
```bash
git clone <repo>
cd carf-keycloak
```

#### 2. Restore .env
```bash
# Copiar .env do backup seguro
cp /secure/backup/.env .env
```

#### 3. Restore backup
```bash
make restore FILE=/secure/backup/keycloak_backup_latest.tar.gz
```

#### 4. Validar
```bash
make health
```

## Teste de Restore

### Executar mensalmente
```bash
# 1. Backup
make backup

# 2. Ambiente de teste
cp docker-compose.dev.yml docker-compose.test.yml
# Editar portas: 8080 -> 8081

docker-compose -f docker-compose.test.yml up -d

# 3. Restore no ambiente de teste
make restore FILE=backups/latest.tar.gz

# 4. Validar
KEYCLOAK_URL=http://localhost:8081 make health

# 5. Cleanup
docker-compose -f docker-compose.test.yml down -v
```

## Backup Offsite

### Upload para S3
```bash
# Instalar AWS CLI
aws s3 cp backups/keycloak_backup_*.tar.gz \
  s3://carf-backups/keycloak/ \
  --storage-class GLACIER
```

### Upload para Azure Blob
```bash
# Instalar Azure CLI
az storage blob upload \
  --account-name carfbackups \
  --container-name keycloak \
  --name keycloak_backup_$(date +%Y%m%d).tar.gz \
  --file backups/keycloak_backup_*.tar.gz
```

## Retenção
- Backups diários: 7 dias
- Backups semanais: 4 semanas
- Backups mensais: 12 meses
- Backups anuais: 7 anos
