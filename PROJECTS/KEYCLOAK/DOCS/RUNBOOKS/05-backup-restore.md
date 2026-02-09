---
type: leaf
status: review
description: "Procedimentos de backup automatico e manual, restore e disaster recovery"
updated: 2026-02-08
---

# Backup e Restore

## Backup Automatico

### Executar Backup

Para executar o backup, navegue até `PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak` e execute `make backup`. Esse Makefile target automatizado realiza o dump do PostgreSQL, exporta o realm do Keycloak, compacta os arquivos em um tarball timestamped e salva o resultado no diretório `backups/`.

### Agenda Automatica via Cron

O backup diário às 2h da manhã é configurado com a entrada cron `0 2 * * * cd /path/to/carf-keycloak && make backup`, garantindo backups regulares sem intervenção manual. Para adicionar limpeza automática de backups antigos, configure um cron semanal com `0 3 * * 0 cd /path/to/carf-keycloak && make backup && find backups/ -mtime +30 -delete`, que remove backups com mais de trinta dias, mantendo a política de retenção organizada e evitando consumo excessivo de disco.

## Backup Manual

### PostgreSQL

O backup manual do PostgreSQL é executado com `docker exec carf-keycloak-postgres-dev pg_dump -U keycloak keycloak > backup.sql`. Esse comando cria um dump SQL completo do database incluindo schema, data, constraints e indexes, permitindo restore para um ponto específico no tempo.

### Realm Export

A exportação do realm é feita em dois passos. Primeiro, execute `docker exec carf-keycloak-dev /opt/keycloak/bin/kc.sh export --realm carf --file /tmp/realm.json --users realm_file`, que exporta a configuração completa do realm incluindo clients, roles, users, grupos e permissions. Em seguida, copie o arquivo para o host com `docker cp carf-keycloak-dev:/tmp/realm.json ./realm-backup.json`. Essa exportação preserva a configuração do Keycloak separadamente do PostgreSQL, permitindo restore seletivo de um realm específico.

## Restore

### Via Script

Para listar os backups disponíveis, execute `ls -lh backups/`, que exibe os arquivos timestamped com tamanhos human-readable facilitando a seleção do backup desejado. O restore é executado com `make restore FILE=backups/keycloak_backup_20260109_143000.tar.gz`, que invoca o Makefile target automatizado para descompactar o tarball, restaurar o dump do PostgreSQL, importar a configuração do realm no Keycloak, reiniciar os serviços e validar os health checks.

### Restore Manual

O restore manual requer três etapas executadas em sequência. Primeiro, pare o Keycloak com `docker-compose -f docker-compose.dev.yml stop keycloak` para garantir que não haja conexões ativas ao database durante o restore. Segundo, restaure o PostgreSQL dropando o database com `docker exec -it carf-keycloak-postgres-dev psql -U keycloak -c "DROP DATABASE keycloak"`, recriando-o com `CREATE DATABASE keycloak` e restaurando o dump com `docker exec -i carf-keycloak-postgres-dev psql -U keycloak keycloak < backup.sql`, que recria o schema completo com todos os dados. Terceiro, reinicie o Keycloak com `docker-compose -f docker-compose.dev.yml start keycloak`, que reconecta ao database com o realm restaurado e permite que os usuários autentiquem normalmente.

## Disaster Recovery

### Cenario de Perda Total do Servidor

O disaster recovery após perda total do servidor segue quatro etapas. Provisione um novo servidor executando `git clone` do repositório seguido por `cd carf-keycloak` para preparar a estrutura. Restaure as variáveis de environment copiando o `.env` do backup seguro com `cp /secure/backup/.env .env`, recuperando configurações, secrets e credenciais. Restaure o backup com `make restore FILE=/secure/backup/keycloak_backup_latest.tar.gz`, que descompacta, recria o database PostgreSQL e importa o realm do Keycloak. Finalmente, valide o funcionamento executando `make health` para verificar endpoints, health checks e autenticação, confirmando que o disaster recovery foi bem-sucedido e o sistema está operacional novamente.

## Teste de Restore

### Execucao Mensal

O teste de restore deve ser executado mensalmente para garantir que os backups são válidos e recuperáveis. O processo inicia com a criação de um backup fresco via `make backup`. Em seguida, prepare um ambiente de teste copiando `docker-compose.dev.yml` para `docker-compose.test.yml` e editando as portas (de 8080 para 8081) para evitar conflitos de port binding, depois suba o ambiente isolado com `docker-compose -f docker-compose.test.yml up -d`.

Restaure no ambiente de teste executando `make restore FILE=backups/latest.tar.gz` para validar que o processo funciona corretamente. Valide os health checks com `KEYCLOAK_URL=http://localhost:8081 make health`, confirmando que autenticação, realm e clients estão funcionando no ambiente restaurado. Ao concluir, faça o cleanup com `docker-compose -f docker-compose.test.yml down -v`, removendo volumes e containers temporários para liberar recursos e manter o ambiente principal intacto.

## Backup Offsite

### Upload para S3

Para armazenar backups offsite na AWS, execute `aws s3 cp backups/keycloak_backup_*.tar.gz s3://carf-backups/keycloak/ --storage-class GLACIER`. Esse comando envia os backups para o S3 Glacier, que oferece armazenamento long-term durável replicado em múltiplas availability zones, garantindo disaster recovery geográfico com proteção contra perda completa do datacenter a um custo efetivo de armazenamento arquival.

### Upload para Azure Blob

Para o Azure, execute `az storage blob upload --account-name carfbackups --container-name keycloak --name keycloak_backup_$(date +%Y%m%d).tar.gz --file backups/keycloak_backup_*.tar.gz`. Esse comando envia o backup para o Azure Blob Storage, garantindo redundância geográfica e proteção offsite dos dados em conformidade com políticas de retenção organizacionais e regulamentações da LGPD que exigem backup obrigatório.

## Retencao

A política de retenção de backups segue uma estratégia escalonada para balancear disponibilidade de restore points com uso eficiente de armazenamento.

| Tipo de Backup | Periodo de Retencao |
|---|---|
| Backups diários | 7 dias |
| Backups semanais | 4 semanas |
| Backups mensais | 12 meses |
| Backups anuais | 7 anos |
