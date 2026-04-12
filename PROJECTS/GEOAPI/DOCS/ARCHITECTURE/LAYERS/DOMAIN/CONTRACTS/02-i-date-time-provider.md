---
type: leaf
status: review
updated: 2026-02-08
---

# IDateTimeProvider

Interface fornecendo data e hora atual de forma injetavel, permitindo testes deterministicos com datas fixas ao inves de depender de DateTime.Now estatico. Em producao retorna valores reais do sistema; em testes permite congelar tempo em data especifica.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| Now | (propriedade) | DateTime | DateTime.UtcNow em producao ou data fixa em testes. |
| Today | (propriedade) | DateTime | Apenas componente de data sem hora. |
| UtcNow | (propriedade) | DateTime | Explicitamente UTC. |

Usada em BaseEntity onde CreatedAt e UpdatedAt sao populados via provider, em validacoes de prazos como LegitimationRequest.Deadline, e em audit logging. Registrada como singleton em producao.
