---
type: leaf
status: review
updated: 2026-02-08
---

# AccessDeniedException

Exception indicando usuario sem permissao para operacao, mapeando para HTTP 403 Forbidden. Herda de DomainException.

Lancada em command handlers apos verificacao de permissoes e em domain services para validacao de ownership.

## Propriedades

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequiredPermission | string | Permissao necessaria: units.delete, legitimation.approve. |
| RequiredRole | Role | Papel minimo: MANAGER, ADMIN. |
| Resource | string | Recurso acessado. |
| Reason | string | Motivo detalhado. |

## Cenarios de Lancamento

| Cenario | Descricao |
| --- | --- |
| Role insuficiente | CADASTRATOR tentando aprovar (requer MANAGER). |
| Sem CommunityAuthorization | Acessar dados de comunidade nao autorizada. |
| Acesso cross-tenant | Tentativa de acessar recurso de outro tenant. |

Middleware retorna ProblemDetails com status 403. Logada como Warning para auditoria de seguranca.
