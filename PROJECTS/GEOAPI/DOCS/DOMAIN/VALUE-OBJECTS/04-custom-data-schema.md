---
type: leaf
status: review
updated: 2026-02-08
---

# CustomData Schema

Value object conceitual definindo schemas de validacao para campos JSONB dinamicos, permitindo configuracao per-tenant de formularios cadastrais customizados. Unit.custom_data armazena campos adicionais especificos de cada prefeitura sem necessidade de alteracao de schema do banco.

## Estrutura do Schema

O schema define campos opcionais com tipos primitivos (texto, numero, booleano), arrays, enumeracoes e objetos aninhados. Cada tenant configura via Tenant.Settings.fields quais campos estao habilitados e obrigatorios.

## Campos Tipicos

| Campo | Tipo | Descricao |
|-------|------|-----------|
| constructionType | enum | MASONRY, WOOD, MIXED. Tipo de construcao. |
| roofMaterial | enum | TILE, CONCRETE_SLAB, ZINC, ASBESTOS, STRAW. Material de cobertura. |
| floors | number | Numero de pavimentos. Minimo 1, maximo 5. |
| hasYard | boolean | Existencia de quintal. |
| hasElectricity | boolean | Energia eletrica. |
| hasPipedWater | boolean | Agua encanada. |
| riskSituation | enum[] | FLOOD, LANDSLIDE, EROSION, NONE. Situacoes de risco. |
| wheelchairAccessible | boolean | Acessibilidade para cadeirante. |

## Validacao em Camadas

| Camada | Descricao |
|--------|-----------|
| Frontend | Valida contra schema configurado para tenant atual, fornecendo feedback imediato. |
| Backend | Re-valida contra mesmo schema garantindo seguranca caso cliente seja bypassado. |
| Database | Valida que campo JSON e sintaticamente valido. Validacao semantica fica em application layer. |

## Schema Evolution

Quando tenant adiciona novo campo, schemaVersion incrementa. Units antigas preservam custom_data no schema antigo sem migration imediata. Application code valida contra schema correspondente a versao da Unit, permitindo coexistencia de multiplas versoes durante transicao gradual.
