---
type: leaf
status: review
updated: 2026-02-08
---

# IDomainEventDispatcher

Interface responsavel por despachar domain events coletados de aggregate roots apos commit bem-sucedido de transacao. Garante que side effects como notificacoes, invalidacao de cache ou jobs executam apenas se mudancas foram persistidas.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| DispatchAsync | IEnumerable de IDomainEvent | Task | Itera eventos, encontra handlers registrados e invoca. |
| DispatchAsync | IDomainEvent singleEvent | Task | Sobrecarga para evento unico. |

Implementada por MediatRDomainEventDispatcher delegando para IMediator do MediatR. Registra exceptions de handlers sem propagar para UnitOfWork, evitando rollback por falha em side effect. Suporta execucao assincrona de handlers.
