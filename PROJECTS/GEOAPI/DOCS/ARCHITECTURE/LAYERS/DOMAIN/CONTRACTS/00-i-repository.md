---
type: leaf
status: review
updated: 2026-02-08
---

# IRepository<T>

Interface generica de repositorio definindo operacoes CRUD padrao para todas entidades do dominio, seguindo padrao Repository de DDD. Garante que logica de acesso a dados permanece isolada na camada Infrastructure, permitindo testabilidade e substituicao de persistencia.

O tipo generico T deve herdar de BaseEntity, garantindo que todas entidades possuem Id, campos de auditoria e soft delete.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| GetByIdAsync | Guid id | T ou null | Busca entidade por ID. |
| GetAllAsync | (nenhum) | List de T | Lista entidades ativas (sem soft delete). |
| FindAsync | Expression predicate | List de T | Busca customizada com lambda. |
| AddAsync | T entity | Task | Adiciona ao contexto sem persistir. |
| Update | T entity | void | Marca como modificada. |
| Delete | T entity | void | Soft delete preenchendo DeletedAt. |
| ExistsAsync | Guid id | bool | Verifica existencia sem carregar. |
| CountAsync | Expression predicate | int | Contagem filtrada. |

Implementada por GenericRepository na Infrastructure usando EF Core DbContext. Integra com IUnitOfWork para transacoes atomicas. Repositorios especializados como IUnitRepository herdam adicionando metodos especificos.
