---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation Validators

Os validators de legitimacao utilizam FluentValidation para validar requests do workflow de legitimacao fundiaria.

## CreateLegitimationRequestValidator

Valida o request de criacao de processo com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| UnitId | Obrigatorio, UUID valido | ID da unidade obrigatorio |

A validacao no FluentValidation e minima pois as pre-condicoes de negocio (unidade APPROVED, titular PROPRIETARIO, ausencia de processo duplicado) sao verificadas no handler com acesso ao repositorio.

## ApproveLegitimationRequestValidator

Valida o request de aprovacao com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| Justification | Obrigatorio, minimo 10 caracteres | Justificativa obrigatoria com minimo 10 caracteres |

## RejectLegitimationRequestValidator

Valida o request de rejeicao com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| Reason | Obrigatorio, minimo 100 caracteres | Motivo obrigatorio com minimo 100 caracteres citando fundamento legal |

A exigencia de 100 caracteres no motivo de rejeicao garante que o gestor forneça fundamento legal substancial conforme requisito da Lei 13.465/2017. Motivos genericos como "Rejeitado" ou "Nao aprovado" sao insuficientes e falham na validacao.

## Validacoes de Negocio no Handler

Alem do FluentValidation, os handlers de legitimacao executam validacoes programaticas que requerem acesso ao banco. O CreateRequestHandler verifica que a unidade tem status APPROVED, que possui ao menos um titular PROPRIETARIO vinculado em unit_holders e que nao existe outro processo ativo para a mesma unidade. O ApproveRequestHandler e RejectRequestHandler verificam que o usuario autenticado possui role manager ou superior.
