---
type: leaf
status: approved
updated: 2026-02-07
---

# UnitHolder

Entidade de juncao representando o vinculo N:N entre Unit e Holder. Cada registro especifica o tipo de relacionamento do titular com a unidade e, para proprietarios, o percentual de participacao na propriedade. Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

O UnitHolder materializa a relacao entre pessoa e imovel, central para todo o processo de regularizacao fundiaria. Cada unidade precisa de ao menos um titular vinculado como PROPRIETARIO com is_primary true para avancar no workflow de aprovacao. O sistema suporta copropriedade (multiplos proprietarios com percentuais somando ate 100) e outros tipos de vinculo que nao conferem direito de propriedade mas sao relevantes para o cadastro.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| UnitId | Guid | nao | FK para Unit. ON DELETE CASCADE. |
| HolderId | Guid | nao | FK para Holder. ON DELETE RESTRICT. |
| RelationshipType | string | nao | Tipo de vinculo. Valores permitidos: PROPRIETARIO (possui direito sobre o imovel), CONJUGE (conjuge do proprietario), MORADOR (reside sem titulo de propriedade), PROCURADOR (representa o proprietario legalmente), HERDEIRO (herdeiro do proprietario falecido). |
| OwnershipPercentage | decimal | sim | Percentual de propriedade entre 0.01 e 100. Obrigatorio quando RelationshipType e PROPRIETARIO. Nao aplicavel para outros tipos de vinculo. |
| IsPrimary | bool | nao | Indica o titular principal responsavel legal pela unidade. Exatamente um titular por unidade deve ser marcado como primary. Default false. |
| CreatedAt | DateTime | nao | Quando o vinculo foi estabelecido. |
| CreatedBy | Guid | nao | Account que criou o vinculo. |

## Relacionamentos

Pertence a uma Unit (obrigatorio). Pertence a um Holder (obrigatorio). O par (UnitId, HolderId) e unico: um mesmo titular nao pode ser vinculado duas vezes a mesma unidade.

## Invariantes de Negocio

A soma de OwnershipPercentage de todos os vinculos PROPRIETARIO de uma mesma unidade nao pode exceder 100. Tentativa de vincular proprietario que exceda o limite retorna erro PERCENTAGE_EXCEEDED.

Exatamente um vinculo por unidade deve ter IsPrimary true. Tentativa de marcar segundo titular como primary retorna erro MULTIPLE_PRIMARY. Ao vincular o primeiro titular de uma unidade, IsPrimary e automaticamente definido como true.

Quando RelationshipType e PROPRIETARIO, OwnershipPercentage e obrigatorio e deve estar entre 0.01 e 100. Para outros tipos, OwnershipPercentage deve ser null.

Holder vinculado como CONJUGE deve ter CPF do conjuge correspondente ao SpouseCpf do titular PROPRIETARIO principal, quando ambos estao presentes.

Apenas titulares PROPRIETARIO contribuem para o calculo de area legitimavel no processo de legitimacao fundiaria.

## Domain Events

Nao emite eventos proprios. Os eventos HolderLinkedEvent e HolderUnlinkedEvent sao emitidos pela entidade Unit ao gerenciar sua colecao de UnitHolders.
