---
type: leaf
status: review
updated: 2026-02-08
---

# BaseAggregateRoot

Classe base que estende BaseEntity adicionando suporte a Domain Events conforme padrao DDD de aggregate roots. Utilizada pelas entidades raiz de agregados que coordenam mudancas em seu grafo de objetos: Unit, Community, Team e LegitimationRequest. Alem de herdar todos os campos e metodos de BaseEntity (Id, timestamps, soft delete, concorrencia otimista), adiciona mecanismo de coleta e dispatch de eventos de dominio.

## Propriedades

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| DomainEvents | IReadOnlyList | Lista somente-leitura de eventos de dominio pendentes que ainda nao foram despachados. Exposta para que a camada de Infrastructure possa processar os eventos apos persistencia. |

## Metodos

| Metodo | Retorno | Descricao |
|--------|---------|-----------|
| AddDomainEvent(IDomainEvent) | void | Adiciona um evento de dominio a lista interna de pendentes. Chamado dentro de metodos de negocio do agregado (ex: ao criar Unit, adiciona UnitCreatedEvent). |
| ClearDomainEvents() | void | Limpa a lista de eventos pendentes. Chamado pela Infrastructure apos despachar todos os eventos com sucesso. |

## Ciclo de Vida dos Eventos

O fluxo de dispatch segue tres etapas: primeiro, o metodo de negocio do agregado chama AddDomainEvent registrando o evento. Em seguida, a camada de Infrastructure persiste as mudancas via SaveChanges dentro de uma transacao. Somente apos o commit bem-sucedido, o IDomainEventDispatcher itera sobre DomainEvents e despacha cada um para seus handlers via MediatR. Por fim, ClearDomainEvents e chamado.

Essa sequencia garante que eventos so sao despachados se a persistencia foi bem-sucedida, evitando notificacoes sobre operacoes que falharam. Handlers podem processar notificacoes, invalidacao de cache, jobs em background e integracao com sistemas externos sem acoplar o dominio a preocupacoes de infraestrutura.
