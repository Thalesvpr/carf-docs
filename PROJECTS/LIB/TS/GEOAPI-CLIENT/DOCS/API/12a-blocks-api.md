---
type: leaf
status: review
updated: 2026-02-08
---

# Blocks API - Gerenciamento de Quadras

A Blocks API fornece operacoes CRUD para quadras, subdivisoes espaciais de comunidades usadas para organizar lotes e unidades habitacionais. Acessada via propriedade blocks da instancia GeoApiClient. Tipo Block importado de @carf/tscore/types conforme [02-types-entities](../../TSCORE/DOCS/API/02-types-entities.md). Para lotes dentro de quadras ver [12b-plots-api](./12b-plots-api.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| GET | /api/blocks | Listar quadras com filtros | 200 | - | todos autenticados |
| GET | /api/blocks/{id} | Buscar quadra por ID | 200 | 404 | todos autenticados |
| POST | /api/blocks | Criar quadra | 201 | 400, 409 | manager+ |
| PATCH | /api/blocks/{id} | Atualizar quadra | 200 | 404, 409 | manager+ |

## list (GET /api/blocks)

Lista quadras com filtros e paginacao. Aceita query params communityId (UUID para filtrar por comunidade), page e limit (paginacao padrao). Retorna PaginatedResponse de Block. Acessivel por todos os usuarios autenticados.

## getById (GET /api/blocks/{id})

Busca quadra por ID. Aceita id string e options.include opcional (array com valores "plots" e/ou "community" para eager loading). Retorna Block com relacionamentos solicitados populados. Lanca NotFoundError 404 se nao existir.

## create (POST /api/blocks)

Cria nova quadra. Aceita CreateBlockDTO:

| Campo | Tipo TS | Obrigatorio | Descricao |
|:------|:--------|:------------|:----------|
| communityId | string | sim | UUID da comunidade pai |
| code | string | sim | Codigo unico dentro da comunidade, maximo 50 caracteres |
| name | string | nao | Nome descritivo opcional, maximo 100 caracteres |
| boundary | GeoJsonPolygon | nao | Perimetro da quadra como GeoJSON Polygon WGS84 |

Response retorna Block com id gerado, area calculada automaticamente a partir do boundary quando fornecido, e timestamps. Constraint UNIQUE em (communityId, code) retorna ConflictError 409 se codigo ja existir na comunidade.

## update (PATCH /api/blocks/{id})

Atualiza quadra existente. Aceita id string e campos de CreateBlockDTO (todos opcionais). Retorna Block atualizado. Recalcula area automaticamente se boundary for alterado.
