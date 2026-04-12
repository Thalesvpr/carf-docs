---
type: leaf
status: approved
updated: 2026-02-07
---

# Domain Events

Domain events desacoplam efeitos colaterais (enviar email, invalidar cache, registrar auditoria, notificar via SignalR) da logica de negocio principal, permitindo adicionar novos handlers sem modificar as entidades ou handlers de commands existentes.

## Estrutura

Cada event e um record imutavel contendo os dados essenciais da ocorrencia: o ID do aggregate que emitiu, o tenant_id para contexto, o timestamp de quando ocorreu e as propriedades relevantes para a acao. UnitCreatedEvent contem UnitId, TenantId, CommunityId, CreatedBy e OccurredAt. HolderLinkedEvent contem UnitId, HolderId, RelationshipType e OccurredAt. UnitStatusChangedEvent contem UnitId, OldStatus, NewStatus, ChangedBy e OccurredAt.

## Coleta e Despacho

Entidades que herdam de BaseAggregateRoot possuem um metodo protegido AddDomainEvent que adiciona o event a uma lista interna temporaria. Quando Unit.Submit() transiciona o status de DRAFT para PENDING_ANALYSIS, o metodo adiciona um UnitStatusChangedEvent a lista. Quando Unit.LinkHolder() vincula um titular, adiciona HolderLinkedEvent.

Os events ficam acumulados na lista interna durante toda a execucao do handler. Apos SaveChangesAsync do DbContext completar com sucesso (transacao commitada), um interceptor do EF Core varre todas as entidades rastreadas que sao aggregate roots, coleta seus domain events pendentes e publica cada um via MediatR.Publish. Isso garante consistencia: eventos so sao despachados se a persistencia funcionou.

## Handlers

Cada event pode ter multiplos handlers independentes processados em paralelo pelo MediatR. UnitStatusChangedEvent tem quatro handlers. O CacheInvalidationHandler invalida o cache Redis da listagem de unidades da comunidade afetada. O AuditLogHandler registra a mudanca de status na tabela audit_logs com old_values contendo o status anterior e new_values contendo o novo. O NotificationHandler envia notificacao via SignalR para os usuarios relevantes (analysts do tenant quando submit, criador da unidade quando approve/reject). O EmailHandler envia email para o criador quando a unidade e aprovada ou rejeitada.

Handlers sao independentes: a falha de um nao afeta os demais. Se o EmailHandler falhar por indisponibilidade do SMTP, o AuditLogHandler e o CacheInvalidationHandler ja executaram com sucesso. O handler com falha entra em retry com politica de 3 tentativas com backoff exponencial. Falhas persistentes apos todas as tentativas sao registradas em log de erro para processamento manual posterior.

## Eventos do Sistema

Os domain events emitidos pelo sistema sao: UnitCreatedEvent ao criar unidade, UnitUpdatedEvent ao atualizar campos, UnitStatusChangedEvent a cada transicao de status, HolderLinkedEvent ao vincular titular, HolderUnlinkedEvent ao desvincular, CorrectionRequestedEvent ao solicitar correcoes, RequestApprovedEvent ao aprovar legitimacao, RequestRejectedEvent ao rejeitar, CertificateIssuedEvent ao emitir certidao, ContestationReceivedEvent ao receber contestacao, SyncConflictEvent ao detectar conflito de sincronizacao e SyncCompletedEvent ao concluir sincronizacao.

## Auditoria Automatica

Um GenericAuditHandler generico subscreve a todos os domain events e registra cada ocorrencia na tabela audit_logs, garantindo trilha de auditoria completa sem necessidade de codigo explicito em cada handler. O registro inclui tipo do evento, dados do payload, account_id do usuario, timestamp, IP de origem e user agent, atendendo requisitos de conformidade LGPD para rastreamento de operacoes sobre dados pessoais.
