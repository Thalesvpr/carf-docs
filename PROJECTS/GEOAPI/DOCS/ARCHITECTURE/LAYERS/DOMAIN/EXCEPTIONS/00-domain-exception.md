---
type: leaf
status: review
updated: 2026-02-08
---

# DomainException

Exception base abstrata para todas excecoes de dominio representando violacao de regra de negocio. Mapeia para HTTP 400 Bad Request por padrao. Subclasses sobrescrevem o codigo HTTP (404, 403, 409).

Fornece estrutura padrao para erros incluindo codigo identificavel, detalhes adicionais e serializacao para API.

## Propriedades

| Campo | Tipo | Descricao |
| --- | --- | --- |
| Message | string | Mensagem descritiva do erro. |
| ErrorCode | string | Codigo unico: UNIT_INVALID_AREA, CPF_ALREADY_EXISTS. |
| Details | Dictionary | Metadados: campo, valor invalido, constraint. |
| HttpStatusCode | int | Codigo HTTP. Default 400. |

## Cenarios de Lancamento

| Cenario | Descricao |
| --- | --- |
| Value object invalido | Cpf, Email, PhoneNumber com formato incorreto. |
| Regra de negocio | Unit sem Holder ao aprovar, area negativa. |
| Transicao invalida | Status APPROVED tentando voltar para DRAFT. |
| Integridade referencial | Deletar Community com Units ativas. |

Capturada por middleware mapeando para ProblemDetails RFC 7807. Logada como Warning.
