---
type: leaf
status: approved
updated: 2026-02-07
---

# Building

Entidade representando uma edificacao dentro de um lote que pode conter multiplas unidades habitacionais. Util para modelar predios, vilas e conjuntos habitacionais onde um unico lote possui varias unidades distintas. Pertence opcionalmente a um Plot e agrega Units que compartilham a mesma estrutura fisica.

## Papel no Dominio

Building e um nivel intermediario opcional na hierarquia Community > Block > Plot > Building > Unit. Nem toda unidade pertence a uma edificacao: casas individuais em lotes independentes vinculam-se diretamente ao lote sem building. A entidade existe para cenarios urbanos densos onde diferenciar a estrutura fisica (predio, vila) das unidades individuais (apartamentos, casas de vila) e necessario para a regularizacao fundiaria. O campo unit_count permite validar que o numero de unidades vinculadas nao exceda a capacidade declarada da edificacao.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| PlotId | Guid | sim | FK para Plot. Nullable pois edificacao pode existir sem lote formalmente demarcado em areas irregulares. |
| UnitCount | int | nao | Numero declarado de unidades na edificacao. Default 1 para casas. |
| BuildingType | string | nao | Tipo da edificacao: CASA, APARTAMENTO, COMERCIAL, MISTO. |
| FloorsCount | int | sim | Numero de andares. Nullable para edificacoes terrreas onde a informacao nao e relevante. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Pertence opcionalmente a um Plot via PlotId. Quando o lote nao esta formalmente demarcado (comum em areas de ocupacao irregular), PlotId e null e a edificacao vincula-se indiretamente a comunidade via as unidades que contem.

Possui colecao de Units vinculadas via building_id na tabela units. Uma unidade pode ou nao estar vinculada a uma edificacao.

## Invariantes de Negocio

BuildingType deve ser um dos valores permitidos: CASA, APARTAMENTO, COMERCIAL, MISTO. Qualquer outro valor e rejeitado com VALIDATION_ERROR.

UnitCount deve ser maior ou igual a 1. O numero de unidades efetivamente vinculadas (com building_id apontando para esta edificacao) nao deve exceder UnitCount, embora essa validacao seja tratada como aviso, nao como bloqueio, pois a contagem declarada pode estar desatualizada.

FloorsCount, quando informado, deve ser maior ou igual a 1.

Building so pode ser excluido (soft delete) se nao houver unidades ativas vinculadas. Tentativa de excluir edificacao com unidades vinculadas retorna erro HAS_UNITS.

## Domain Events

BuildingCreatedEvent emitido ao criar edificacao. BuildingUpdatedEvent emitido ao atualizar dados. Nao emite eventos de vinculacao de unidades pois esses sao responsabilidade da entidade Unit ao definir seu building_id.
