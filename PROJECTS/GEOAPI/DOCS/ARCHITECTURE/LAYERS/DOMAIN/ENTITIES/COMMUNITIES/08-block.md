---
type: leaf
status: approved
updated: 2026-02-07
---

# Block

Entidade representando quadra urbana, subdivisao espacial de uma Community. Organiza o territorio em areas menores contendo multiplos lotes (Plots). Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

Blocos sao opcionais. Comunidades urbanas formais tipicamente possuem blocos organizados em quadras com codigos como QD-01 ou QUADRA-A. Comunidades rurais ou assentamentos informais podem nao ter blocos, com unidades vinculadas diretamente a comunidade. Quando presente, o bloco facilita organizacao cadastral, geracao de plantas por quadra e relatorios agrupados.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| CommunityId | Guid | nao | FK para Community. Hierarquia Community maior que Block maior que Plot. |
| Code | string | nao | Codigo unico dentro da comunidade. |
| Name | string | sim | Nome descritivo opcional. |
| Boundary | Polygon | sim | Perimetro da quadra em WGS84 SRID 4326. |
| Area | decimal | sim | Area em metros quadrados. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Pertence a uma Community (obrigatorio). Contem colecao de Plots filhos. Units podem referenciar BlockId diretamente como desnormalizacao para queries eficientes.

## Invariantes de Negocio

Code unico dentro da mesma comunidade. Boundary dos Plots filhos deve estar contido dentro do boundary do bloco quando ambos estao preenchidos.
