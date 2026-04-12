---
type: leaf
status: approved
updated: 2026-02-07
---

# Plot

Entidade representando lote individual dentro de um Block, a parcela cadastral minima. Pode ou nao estar vinculado a uma Unit, permitindo representar lotes vagos sem ocupacao. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

O lote e a divisao formal do territorio onde uma unidade habitacional pode estar construida. Nem toda unidade tem lote (assentamentos informais) e nem todo lote tem unidade (lotes vagos). Essa flexibilidade permite representar a realidade mista dos assentamentos brasileiros.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| BlockId | Guid | nao | FK para Block. Hierarquia Block maior que Plot. |
| Code | string | nao | Codigo unico dentro do bloco. |
| Boundary | Polygon | sim | Perimetro do lote em WGS84 SRID 4326. |
| Area | decimal | sim | Area em metros quadrados. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Pertence a um Block (obrigatorio). Pode ter uma Unit vinculada via PlotId. Pode ter um Building vinculado.

## Invariantes de Negocio

Code unico dentro do mesmo bloco. Boundary deve estar contido dentro do boundary do bloco pai quando ambos preenchidos.
