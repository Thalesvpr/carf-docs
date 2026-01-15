# Backup e Restore

## Backup Automático

### Executar backup

Executar backup navegando para PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak com cd seguido por make backup invocando Makefile target automatizado executando dump PostgreSQL export realm Keycloak compactando arquivos tarball timestamped salvando em diretório backups/.

### Agenda automática (cron)

Configurar backup diário às 2am com cron job zero dois asterisco asterisco asterisco navegando cd /path/to/carf-keycloak executando make backup garantindo backups regulares sem intervenção manual. Configurar backup semanal com limpeza de backups antigos zero três asterisco asterisco zero executando make backup seguido por find backups/ menos mtime mais trinta menos delete removendo backups com mais de trinta dias mantendo retenção política organizada evitando consumo excessivo disco.

## Backup Manual

### PostgreSQL

Backup manual PostgreSQL executando docker exec carf-keycloak-postgres-dev pg_dump menos U keycloak keycloak redirecionando output para backup.sql criando dump SQL completo database incluindo schema data constraints indexes permitindo restore ponto específico tempo.

### Realm export

Exportar realm executando docker exec carf-keycloak-dev /opt/keycloak/bin/kc.sh export especificando menos menos realm carf menos menos file /tmp/realm.json menos menos users realm_file exportando configuração realm completa incluindo clients roles users grupos permissions seguido por docker cp carf-keycloak-dev:/tmp/realm.json ./realm-backup.json copiando export do container para host filesystem preservando configuração Keycloak separadamente de PostgreSQL permitindo restore seletivo realm específico.

## Restore

### Via script

Listar backups disponíveis executando ls menos lh backups/ exibindo arquivos timestamped com tamanhos human-readable facilitando seleção backup específico. Restore do backup mais recente executando make restore FILE igual backups/keycloak_backup_20260109_143000.tar.gz invocando Makefile target automatizado descompactando tarball restaurando PostgreSQL dump importando realm configuration Keycloak reiniciando serviços validando health checks.

### Manual

Restore manual requer três etapas sendo primeiro parar Keycloak executando docker-compose menos f docker-compose.dev.yml stop keycloak garantindo sem conexões ativas database durante restore, segundo restaurar PostgreSQL dropando database executando docker exec menos it carf-keycloak-postgres-dev psql menos U keycloak menos c DROP DATABASE keycloak seguido por recriar executando CREATE DATABASE keycloak e restaurar dump executando docker exec menos i carf-keycloak-postgres-dev psql menos U keycloak keycloak redirecionando input de backup.sql recriando schema completo data, terceiro restart Keycloak executando docker-compose menos f docker-compose.dev.yml start keycloak reconectando database realm restaurado usuários autenticando normalmente.

## Disaster Recovery

### Cenário: Perda total do servidor

Disaster recovery após perda total do servidor requer quatro etapas sendo primeiro provisionar novo servidor executando git clone do repositório seguido por cd carf-keycloak preparando estrutura, segundo restaurar environment variables copiando .env do backup seguro executando cp /secure/backup/.env .env recuperando configurações secrets credenciais, terceiro restaurar backup executando make restore FILE igual /secure/backup/keycloak_backup_latest.tar.gz descompactando recriando PostgreSQL database importando realm Keycloak, quarto validar funcionamento executando make health verificando endpoints health checks autenticação funcionando confirming disaster recovery bem-sucedido sistema operacional novamente.

## Teste de Restore

### Executar mensalmente

Teste de restore executado mensalmente seguindo cinco etapas garantindo backups válidos recuperáveis sendo primeiro criar backup executando make backup gerando snapshot atual, segundo preparar ambiente de teste copiando docker-compose.dev.yml para docker-compose.test.yml editando portas alterando oito zero oito zero para oito zero oito um evitando conflitos port binding seguido por docker-compose menos f docker-compose.test.yml up menos d subindo ambiente isolado, terceiro restaurar no ambiente de teste executando make restore FILE igual backups/latest.tar.gz validando processo restore funciona corretamente, quarto validar health executando KEYCLOAK_URL igual http://localhost:8081 make health confirmando autenticação realm clients funcionando ambiente restaurado, quinto cleanup executando docker-compose menos f docker-compose.test.yml down menos v removendo volumes containers temporários liberando recursos mantendo ambiente principal intacto validação concluída com sucesso.

## Backup Offsite

### Upload para S3

Upload para AWS S3 Glacier instalando AWS CLI seguido por executar aws s3 cp backups/keycloak_backup_asterisco.tar.gz especificando s3://carf-backups/keycloak/ com menos menos storage-class GLACIER armazenando backups offsite long-term durável replicado múltiplas availability zones garantindo disaster recovery geográfico proteção contra perda datacenter completo custo efetivo armazenamento arquival.

### Upload para Azure Blob

Upload para Azure Blob Storage instalando Azure CLI seguido por executar az storage blob upload especificando menos menos account-name carfbackups menos menos container-name keycloak menos menos name keycloak_backup_$(date mais porcento Y porcento m porcento d).tar.gz menos menos file backups/keycloak_backup_asterisco.tar.gz enviando backup para Azure cloud storage redundância geográfica proteção dados offsite garantindo business continuity compliance políticas retenção organizacionais regulamentações LGPD backup obrigatório.

## Retenção
- Backups diários: 7 dias
- Backups semanais: 4 semanas
- Backups mensais: 12 meses
- Backups anuais: 7 anos
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
