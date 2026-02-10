---
type: leaf
status: review
updated: 2026-02-08
---

# ConflictException

Exception indicando conflito de unicidade ou concorrencia, mapeando para HTTP 409 Conflict. Herda de DomainException.

Permite frontend tratar retentativas ou resolucao manual, especialmente em cenarios de optimistic locking com version.

## Propriedades

| Campo | Tipo | Descricao |
| --- | --- | --- |
| ConflictType | string | DUPLICATE_CPF, DUPLICATE_CODE, CONCURRENT_MODIFICATION. |
| ConflictingValue | string | Valor que causou conflito. |
| ExistingResourceId | Guid | ID do recurso conflitante. |
| Field | string | Campo conflitante. |

## Cenarios de Lancamento

| Cenario | Descricao |
| --- | --- |
| CPF duplicado | Holder com mesmo CPF no tenant (UNIQUE tenant_id, cpf). |
| Codigo duplicado | Unit com code ja existente (UNIQUE tenant_id, code). |
| Concorrencia | version difere entre read e write. |
| Integridade | Deletar Community com Units vinculadas. |

Middleware retorna ProblemDetails com status 409. ConcurrentModification pode ser retentada com backoff.
