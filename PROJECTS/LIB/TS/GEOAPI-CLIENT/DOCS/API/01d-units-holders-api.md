---
type: leaf
status: review
updated: 2026-02-08
---

# Units API - Gestao de Titulares na Unidade

Metodos de vinculacao e gestao de titulares dentro do contexto de uma unidade habitacional, acessiveis via api.units conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md). Tipo RelationshipType documentado em [04-types-enums](../../TSCORE/DOCS/API/04-types-enums.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| GET | /api/units/{id}/holders | Listar titulares vinculados | 200 | 404 | todos autenticados |
| POST | /api/units/{id}/holders | Vincular titular a unidade | 201 | 400 PERCENTAGE_EXCEEDED, 400 MULTIPLE_PRIMARY, 409 DUPLICATE | todos autenticados |
| PATCH | /api/units/{id}/holders/{holderId} | Atualizar vinculo | 200 | 400 PERCENTAGE_EXCEEDED, 400 MULTIPLE_PRIMARY | todos autenticados |
| DELETE | /api/units/{id}/holders/{holderId} | Desvincular titular | 204 | - | todos autenticados |

## getHolders

O metodo getHolders aceita unitId string e retorna Promise de array de UnitHolder. Cada UnitHolder contem id do vinculo, unitId, holderId, relationshipType, ownershipPercentage, isPrimary e createdAt, alem do objeto holder populado com dados completos do titular.

## addHolder

O metodo addHolder aceita unitId string e AddHolderDTO, retornando Promise de UnitHolder criado.

| Campo | Tipo TS | Obrigatorio | Descricao |
|:------|:--------|:------------|:----------|
| holderId | string | sim | UUID do titular existente no sistema |
| relationshipType | RelationshipType | sim | PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR ou HERDEIRO |
| ownershipPercentage | number | condicional | Decimal entre 0 e 100, obrigatorio quando PROPRIETARIO |
| isPrimary | boolean | nao | Titular principal, default false |

Regras de validacao: o holderId deve referenciar um titular existente no tenant. Constraint UNIQUE em (unitId, holderId) impede vinculo duplicado, retornando ConflictError 409 com code DUPLICATE. A soma de ownershipPercentage de todos os vinculos tipo PROPRIETARIO da unidade nao pode exceder 100, retornando ValidationError 400 com code PERCENTAGE_EXCEEDED. Apenas um titular por unidade pode ter isPrimary true, tentativa de definir segundo retorna ValidationError 400 com code MULTIPLE_PRIMARY.

## updateHolder

O metodo updateHolder aceita unitId string, holderId string e campos parciais do AddHolderDTO (sem holderId). Retorna Promise de UnitHolder atualizado. Permite alterar relationshipType, ownershipPercentage ou isPrimary, respeitando as mesmas regras de validacao do addHolder.

## removeHolder

O metodo removeHolder aceita unitId string e holderId string, retornando void (204 No Content). Remove o vinculo entre titular e unidade sem deletar o titular do sistema.
