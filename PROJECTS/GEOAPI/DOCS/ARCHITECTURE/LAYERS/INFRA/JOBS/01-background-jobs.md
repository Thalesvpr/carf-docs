---
type: leaf
status: active
updated: 2026-02-07
---

# Background Jobs

A GEOAPI utiliza Hangfire com storage PostgreSQL para processamento assincrono. O servidor e configurado com tres filas de prioridade: critical, default e low. O numero de workers e duas vezes o numero de processadores da maquina. O intervalo de polling das filas e 15 segundos.

## Jobs Definidos

### ReportGenerationJob

Executa na fila default. Recebe o id do relatorio, carrega a entidade do banco, gera o PDF via servico de geracao, faz upload do arquivo para o storage S3 com nome "report-{id}.pdf", atualiza o status do relatorio para concluido com a chave do arquivo e notifica o usuario solicitante.

### NotificationJob

Oferece dois metodos. SendEmailNotification executa na fila critical: carrega o usuario pelo id e envia email com assunto e corpo informados. SendBulkNotifications executa na fila low: itera sobre a lista de userIds e enfileira um SendEmailNotification individual para cada usuario.

### DataCleanupJob

Oferece dois metodos na fila low. CleanupExpiredTokens deleta tokens expirados do banco. CleanupTempFiles lista arquivos temporarios com mais de um dia no storage e os remove individualmente.

## Jobs Recorrentes

| Job | Metodo | Cron | Horario UTC |
|-----|--------|------|-------------|
| cleanup-expired-tokens | CleanupExpiredTokens | Diario | 03:00 |
| cleanup-temp-files | CleanupTempFiles | Diario | 04:00 |

## Enfileiramento

Jobs podem ser disparados de duas formas. Fire-and-forget com BackgroundJob.Enqueue executa imediatamente na proxima oportunidade. Delayed com BackgroundJob.Schedule aceita um TimeSpan para execucao futura, utilizado por exemplo para enviar lembretes apos 24 horas.

## Tabela Completa de Jobs

| Job | Classe | Fila | Trigger | Cron | Timeout | Retry | Descricao |
|-----|--------|------|---------|------|---------|-------|-----------|
| OrtophotoProcessing | OrtophotoProcessingJob | critical | Fire-and-forget (apos upload) | - | 30min | 3x com backoff | Processa GeoTIFF: reprojecao, tile generation, thumbnail |
| ReportGeneration | ReportGenerationJob | default | Fire-and-forget (solicitacao usuario) | - | 10min | 2x | Gera PDF/CSV/Shapefile |
| NotificationEmail | NotificationJob | critical | Fire-and-forget | - | 1min | 3x | Envia email individual |
| NotificationBulk | NotificationJob | low | Fire-and-forget | - | 5min | 1x | Enfileira emails em massa |
| CleanupExpiredTokens | DataCleanupJob | low | Recurring | 0 3 * * * (3h UTC) | 5min | 0 | Remove tokens/sessions expirados |
| CleanupTempFiles | DataCleanupJob | low | Recurring | 0 4 * * * (4h UTC) | 10min | 0 | Remove arquivos temp > 24h |
| CleanupOrphanedFiles | DataCleanupJob | low | Recurring | 0 5 * * 0 (dom 5h) | 30min | 0 | Remove arquivos S3 sem referencia no banco |
| SyncStaleDetection | SyncMonitorJob | default | Recurring | */15 * * * * (cada 15min) | 2min | 0 | Detecta devices sem sync > 7 dias, notifica coordenador |
| CommunityStatsRefresh | StatsRefreshJob | low | Recurring | 0 */6 * * * (cada 6h) | 5min | 1x | Recalcula estatisticas agregadas de comunidades |

### Detalhes de Jobs Especificos

**OrtophotoProcessingJob**: Recebe o ID da ortofoto recem-uploadada. Etapas: (1) download do GeoTIFF original do S3, (2) validacao de formato e CRS (deve ser EPSG:4674 SIRGAS 2000), (3) reprojecao se necessario via GDAL, (4) geracao de tiles para visualizacao web (256x256 PNG), (5) geracao de thumbnail 512px, (6) upload dos artefatos processados para S3, (7) atualizacao do status da ortofoto para "processed". Em caso de falha, status atualizado para "failed" com mensagem de erro.

**SyncMonitorJob**: Consulta a tabela de sync_logs para encontrar devices cuja ultima sincronizacao foi ha mais de 7 dias. Para cada device encontrado, enfileira uma NotificationEmail para o coordenador da equipe responsavel. Registra alerta no log estruturado com nivel Warning.

**CommunityStatsRefresh**: Para cada comunidade ativa, recalcula: total de unidades, unidades por status, total de titulares, area total georreferenciada, percentual de cobertura. Grava resultado no cache Redis com chave `community:{id}:stats` e TTL de 6 horas.

## Monitoramento

O Hangfire Dashboard esta acessivel em `/hangfire`, protegido por politica de autorizacao que exige role `admin` ou superior.

### Funcionalidades do Dashboard

- **Filas**: visualizar jobs enfileirados, em execucao, concluidos e falhados por fila (critical, default, low)
- **Retry manual**: clicar no job falhado e selecionar Requeue para re-enfileirar
- **Metricas**: jobs processados por hora, tempo medio de execucao, taxa de falha
- **Servidores**: lista de workers ativos com capacidade e filas processadas

### Alertas

| Condicao | Severidade | Canal | Acao |
|----------|-----------|-------|------|
| Job na fila critical > 5min sem processar | Critical | Slack #alerts-critical | Verificar workers ativos |
| Job falhado em fila critical | High | Slack #alerts-high | Investigar logs do job |
| Fila default > 100 jobs pendentes | Warning | Slack #alerts-warning | Considerar scale up de workers |
| Job recorrente nao executou no horario | Warning | Slack #alerts-warning | Verificar saude do servidor Hangfire |

## Configuracao de Retry

O decorator `AutomaticRetry` configura o comportamento de re-tentativa por job:

```
[AutomaticRetry(Attempts = 3, DelaysInSeconds = new[] { 60, 300, 900 })]
```

Delay pattern: 1min, 5min, 15min (backoff exponencial). Apos todas as tentativas esgotadas, o job transiciona para o estado **Failed** e permanece visivel no dashboard para intervencao manual.

### Tabela de Retry por Job

| Job | Attempts | Delays (segundos) | Comportamento apos falha final |
|-----|----------|-------------------|-------------------------------|
| OrtophotoProcessingJob | 3 | 60, 300, 900 | Failed + alerta Slack |
| ReportGenerationJob | 2 | 60, 300 | Failed + notifica usuario |
| NotificationJob (email) | 3 | 30, 60, 300 | Failed (email nao enviado) |
| NotificationJob (bulk) | 1 | 60 | Failed (parcialmente enviado) |
| DataCleanupJob | 0 | - | Failed (proximo cron retenta) |
| SyncMonitorJob | 0 | - | Failed (proximo cron retenta) |
| StatsRefreshJob | 1 | 300 | Failed (dados usam cache anterior) |

## Boas Praticas

1. **Idempotencia**: todo job deve ser idempotente — re-executar nao deve causar duplicatas ou efeitos colaterais
2. **Timeout**: sempre definir timeout maximo para evitar jobs pendurados
3. **Logging estruturado**: cada job deve logar inicio, progresso e conclusao com correlation ID
4. **Tenant context**: jobs que acessam dados devem configurar o TenantContext antes de executar queries
5. **Transacoes**: jobs de longa duracao devem usar transacoes parciais com checkpoints, nao uma unica transacao
