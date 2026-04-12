---
type: leaf
status: review
updated: 2026-02-07
---

# Plots API - Gerenciamento de Lotes

A Plots API fornece operacoes CRUD para lotes e vinculacao com unidades habitacionais. Lotes sao subdivisoes de quadras dentro de comunidades. Acessada via propriedade **plots** da instancia GeoApiClient. Tipo Plot importado de @carf/tscore/types. Para quadras ver [12a-blocks-api](./12a-blocks-api.md).

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/plots | Listar lotes |
| GET | /api/plots/:id | Buscar por ID |
| POST | /api/plots | Criar lote |
| PATCH | /api/plots/:id | Atualizar lote |
| POST | /api/plots/:id/unit | Vincular unidade a lote |

## list()

Lista lotes com filtros. Aceita query opcional com blockId, communityId, page e limit, retornando PaginatedResponse de Plot.

## getById()

Busca lote por ID. Aceita id (string) e options.include opcional (array com valores "block" e/ou "unit"). Retorna Plot com relacionamentos solicitados.

## create()

Cria novo lote. Aceita CreatePlotDTO, retorna Plot.

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| code | string | Sim | Codigo do lote |
| blockId | string | Sim | Identificador da quadra |
| communityId | string | Sim | Identificador da comunidade |
| geometry | string | Nao | Geometria em WKT ou GeoJSON |
| area | number | Nao | Area em metros quadrados |

## update()

Atualiza lote existente. Aceita id (string) e objeto com campos de CreatePlotDTO (todos opcionais) mais version (number, obrigatorio) para concorrencia otimista. Retorna Plot atualizado.

## linkUnit()

Vincula unidade habitacional a um lote. Aceita plotId e unitId (ambos string), retorna Plot atualizado com propriedade unitId refletindo o vinculo.
