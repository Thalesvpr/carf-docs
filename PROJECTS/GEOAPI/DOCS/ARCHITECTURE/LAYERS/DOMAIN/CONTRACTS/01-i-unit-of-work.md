---
type: leaf
status: review
updated: 2026-02-08
---

# IUnitOfWork

Interface definindo controle de transacao agrupando multiplas operacoes de repositorios em transacao atomica, seguindo padrao Unit of Work. Garante que todas mudancas sejam persistidas juntas ou nenhuma, mantendo consistencia de dados.

Apos SaveChanges bem-sucedido, domain events sao despachados via IDomainEventDispatcher para handlers processarem side effects.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| SaveChangesAsync | (nenhum) | int | Persiste mudancas, despacha events, retorna entidades afetadas. |
| BeginTransactionAsync | (nenhum) | Task | Inicia transacao explicita. |
| CommitTransactionAsync | (nenhum) | Task | Confirma transacao explicita. |
| RollbackTransactionAsync | (nenhum) | Task | Reverte transacao explicita. |
| Dispose | (nenhum) | void | Libera recursos do contexto. |

Implementada por UnitOfWork encapsulando DbContext do EF Core. Intercepta SaveChanges para popular AuditLog automaticamente e despachar domain events apos commit.
