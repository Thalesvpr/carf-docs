---
type: leaf
status: review
updated: 2026-02-08
---

# ValidationException

Exception para validacao de dados indicando valor invalido ou formato incorreto. Herda de DomainException mapeando para HTTP 400. Agrega multiplos campos invalidos em unica resposta.

Integra com FluentValidation convertendo failures em ValidationException com todos campos agregados.

## Propriedades

| Campo | Tipo | Descricao |
| --- | --- | --- |
| Errors | Dictionary | Mapeia campo para lista de mensagens de erro. |
| Field | string | Campo especifico quando erro unico. |
| ValidationErrorCode | string | INVALID_FORMAT, OUT_OF_RANGE, REQUIRED_FIELD. |

## Cenarios de Lancamento

| Cenario | Descricao |
| --- | --- |
| Cpf invalido | Digitos verificadores falham no Mod11. |
| Email invalido | Formato fora do RFC 5322. |
| Area negativa | Unit.SetArea() com valor menor que zero. |
| Campos obrigatorios | Holder sem full_name ou birth_date. |

Middleware retorna ProblemDetails com errors dictionary para frontend exibir proximos aos campos.
