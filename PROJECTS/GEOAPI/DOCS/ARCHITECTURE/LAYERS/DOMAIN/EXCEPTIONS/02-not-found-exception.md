---
type: leaf
status: review
updated: 2026-02-08
---

# NotFoundException

Exception indicando entidade nao encontrada por identificador, mapeando para HTTP 404. Herda de DomainException.

Lancada em repositories quando GetByIdAsync retorna null, garantindo que camadas superiores nunca recebem null.

## Propriedades

| Campo | Tipo | Descricao |
| --- | --- | --- |
| EntityType | string | Tipo: Unit, Holder, Community. |
| EntityId | Guid | Identificador nao encontrado. |
| SearchCriteria | Dictionary | Criterios quando busca nao e por ID. |

## Cenarios de Lancamento

| Cenario | Descricao |
| --- | --- |
| GetByIdAsync null | Unit, Holder, Community nao encontrados. |
| GetByCpfAsync vazio | Holder nao encontrado por CPF. |
| FK inexistente | Unit referenciando community_id inexistente. |
| Soft-deleted | Registro com deleted_at preenchido. |

Middleware retorna ProblemDetails com status 404. Logada como Information.
