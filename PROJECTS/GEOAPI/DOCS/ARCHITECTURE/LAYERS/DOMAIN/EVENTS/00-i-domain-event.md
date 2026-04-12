---
type: leaf
status: review
updated: 2026-02-08
---

# IDomainEvent

Interface marcadora base para todos os domain events do sistema, indicando que uma classe representa evento de dominio significativo emitido por aggregate root quando mudanca importante ocorre. Permite comunicacao desacoplada entre agregados e disparo de side effects apos persistencia bem-sucedida.

A interface nao define metodos ou propriedades obrigatorias, servindo como contrato comum que permite IDomainEventDispatcher processar qualquer evento genericamente via polimorfismo. Por convencao, todos os eventos incluem propriedades padrao.

## Propriedades por Convencao

| Campo | Tipo | Descricao |
| --- | --- | --- |
| OccurredAt | DateTime | Timestamp UTC quando evento ocorreu. |
| EntityId | Guid | Identificador da entidade que emitiu evento. |
| TenantId | Guid | Tenant do contexto para isolamento multi-tenant. |
| EventId | Guid | Identificador unico do evento para deduplicacao. |

## Ciclo de Vida

Eventos sao adicionados a colecao DomainEvents em BaseAggregateRoot via metodo protegido AddDomainEvent() durante execucao de metodos de negocio. Sao despachados apenas APOS commit bem-sucedido de transacao via IUnitOfWork.SaveChangesAsync(), garantindo que handlers executam apenas se mudancas foram persistidas.

## Implementacoes

Implementada por todas as classes de evento do dominio como UnitCreatedEvent, HolderLinkedEvent, SyncConflictEvent, CommunityCreatedEvent, RequestSubmittedEvent, CertificateIssuedEvent, entre outros. Cada implementacao adiciona propriedades especificas do contexto.
