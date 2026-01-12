# JOBS

Background jobs Hangfire do GEOAPI executando processos assíncronos fora do request cycle HTTP incluindo envio notificações batch, geração relatórios pesados, sincronização sistemas legados e manutenção dados temporários. Jobs scheduled rodam periodicamente (hourly, daily, weekly) via cron expressions para limpeza sessions expiradas, invalidação cache stale, reprocessamento legitimations pendentes e backup metadata. Fire-and-forget jobs enfileirados sob demanda processam uploads documentos (virus scan, OCR, metadata extraction), envio emails confirmação e webhooks integrações externas com retry automático 3x com backoff exponencial quando falha. Delayed jobs agendam execução futura para reminders notificações (SLA approaching, approval pending 7 days) e jobs continuations encadeiam processamento multi-step onde output de um job alimenta input do próximo (generate report → upload S3 → send email with link). Dashboard Hangfire integrado permite monitoring manual retry de failed jobs e visualização estatísticas throughput latency fila por tipo job.

## Arquivos Principais (a criar)

**Scheduled Jobs:**
- 01-cleanup-sessions-job.md - Limpeza daily sessões expiradas
- 02-process-pending-legitimations-job.md - Reprocessamento hourly
- 03-generate-reports-job.md - Relatórios semanais batch

**Fire-and-Forget:**
- 04-document-processing-job.md - Virus scan e OCR async
- 05-send-notification-job.md - Emails e push notifications
- 06-webhook-delivery-job.md - Integrações externas

**Advanced:**
- 07-job-retry-policies.md - Backoff e dead letter queue
- 08-job-monitoring.md - Dashboard e alerting

---

**Última atualização:** 2026-01-12
