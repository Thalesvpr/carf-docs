---
type: leaf
status: approved
updated: 2026-02-07
---

# Validacao de Edificacao

Regras de validacao para a entidade Edificacao (Building), nivel intermediario entre Lote e Unidade na hierarquia.

## Hierarquia

| Nivel | Entidade | Contido em |
|-------|----------|-----------|
| 1 | Tenant | Raiz |
| 2 | Community | Tenant |
| 3 | Block | Community |
| 4 | Plot | Block |
| 5 | Building | Plot |
| 6 | Unit | Building |

Um lote pode conter multiplas edificacoes. Cada edificacao contem uma ou mais unidades.

## Campos Obrigatorios

| Campo | Tipo | Obrigatorio | Regra |
|-------|------|-------------|-------|
| code | string | Sim | Unico dentro do lote (ex: "ED-A", "ED-B") |
| type | enum | Sim | HOUSE, APARTMENT_BUILDING, WAREHOUSE, COMMERCIAL, MIXED, OTHER |
| typeDescription | string | Condicional | Obrigatorio se type = OTHER |
| plotId | string | Sim | UUID do lote pai |
| communityId | string | Sim | UUID da comunidade |
| tenantId | string | Sim | UUID do tenant |

## Campos Opcionais

| Campo | Tipo | Descricao |
|-------|------|-----------|
| floors | number | Numero de pavimentos (minimo 1) |
| material | enum | MASONRY, WOOD, MIXED, METAL, OTHER |
| materialDescription | string | Obrigatorio se material = OTHER |
| builtArea | number | Area construida em m2 |
| constructionYear | number | Ano de construcao (aproximado) |
| blockId | string | UUID da quadra (opcional) |
| observations | string | Observacoes livres |

## Tipos de Edificacao

| Tipo | Descricao |
|------|-----------|
| HOUSE | Casa terrea ou sobrado unifamiliar |
| APARTMENT_BUILDING | Predio com multiplas unidades |
| WAREHOUSE | Galpao ou deposito |
| COMMERCIAL | Edificacao comercial |
| MIXED | Uso misto (comercial + residencial) |
| OTHER | Outro tipo (requer descricao) |

## Materiais de Construcao

| Material | Descricao |
|----------|-----------|
| MASONRY | Alvenaria (tijolos, blocos) |
| WOOD | Madeira |
| MIXED | Materiais mistos |
| METAL | Estrutura metalica |
| OTHER | Outro material (requer descricao) |

## Regra do Campo "Outros"

Quando `type = OTHER` ou `material = OTHER`, o campo descritivo correspondente torna-se obrigatorio. Nao permite salvar sem preencher a descricao.

## Relacao com Unidades

- Uma edificacao pode ter 0 ou mais unidades
- Ao deletar edificacao, unidades ficam orfas (validar antes)
- Edificacao sem unidades e permitida (cadastro em andamento)

## Codigo Unico

O campo `code` deve ser unico dentro do lote. Sugestao de formato:
- Casa unica: "CASA"
- Multiplas edificacoes: "ED-A", "ED-B", "ED-C"
- Predios: "BLOCO-1", "BLOCO-2"

## Referencia

- Conceito: `CENTRAL/DOMAIN/CONCEPTS/38-building.md`
- TypeScript: `@carf/tscore` → `Building`
