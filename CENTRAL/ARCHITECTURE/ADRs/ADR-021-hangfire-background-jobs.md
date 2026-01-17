# ADR-021: Escolha do Hangfire para Background Jobs

Decisão arquitetural escolhendo Hangfire como solução de background job processing para backend GEOAPI justificada por integração nativa com .NET eliminando necessidade de message broker externo simplificando arquitetura, persistent storage em PostgreSQL garantindo jobs não sejam perdidos em restart mantendo reliability, dashboard web integrado fornecendo observability de jobs (succeeded failed processing scheduled) sem ferramentas externas, automatic retry com exponential backoff em falhas transientes resiliente a issues temporários de database/network, scheduled jobs (cron) para tasks periódicos (sync dados externos nightly reports cleanup old data), fire-and-forget jobs para tasks assíncronas (enviar email processar imagem gerar relatório) sem bloquear request HTTP, delayed jobs executando em momento futuro específico (ex: reminder 24h após cadastro), recurring jobs com cron expressions flexíveis, e ausência de infraestrutura adicional (RabbitMQ Kafka Redis Queue) reduzindo complexidade operacional.

Hangfire especificamente adequado para workloads não críticos onde eventual execution é aceitável versus message broker real-time, suficiente para CARF requirements de processamento assíncrono de relatórios sincronização notificações.

Alternativas consideradas incluem Quartz.NET (rejeitado por ausência de dashboard e persistence configuration complexa), Azure Functions (rejeitado por vendor lock-in e custo per-execution), AWS Lambda (rejeitado por vendor lock-in), MassTransit + RabbitMQ (rejeitado por overhead arquitetural desnecessário para use cases simples), background services ASP.NET Core (rejeitado por ausência de persistence retry dashboard), e Azure Storage Queues (rejeitado por lock-in Azure).

Consequências positivas incluem simplicidade de implementação, dashboard built-in, reliability com persistence, zero infra adicional, e custo zero open-source. Consequências negativas incluem throughput limitado comparado a message brokers dedicados (suficiente para escala atual <10k jobs/day), impossibilidade de inter-service communication exigindo eventual migration para RabbitMQ em arquitetura microservices futura, e latency ocasional em job pickup (~5-15s).

Configuração utiliza Hangfire 1.8+ com PostgreSQL storage, dashboard habilitado em `/hangfire` com authorization exigindo role ADMIN, recurringjobs para sync diário, e retention policy deletando succeeded jobs após 7 dias mantendo database compacto.

Status aprovado e implementado desde 2024-Q3.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + Backend
**Última revisão:** 2025-01-10
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
