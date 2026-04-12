---
type: leaf
status: approved
updated: 2026-02-07
---

# LayerFeature

Entidade representando geometria individual dentro de uma Layer com atributos descritivos em formato JSONB extensivel. Cada feature e um ponto, linha ou poligono com propriedades customizaveis por tenant. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

LayerFeatures armazenam dados espaciais customizados sem necessidade de alteracao de schema. As propriedades JSONB permitem atributos livres como nivel de risco, populacao afetada, diametro de tubulacao ou qualquer outro dado relevante para o contexto do municipio. Indexacao espacial via GiST permite queries rapidas de proximidade, intersecao e contencao.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| LayerId | Guid | nao | FK para Layer pai. |
| Geometry | geometry | nao | Geometria PostGIS. Tipo deve corresponder ao LayerType da camada pai (POINT, LINESTRING ou POLYGON). |
| Properties | JsonDocument | sim | Atributos descritivos em formato JSONB livre. Exemplos: risco "alto", populacao_afetada 150, diametro_mm 100. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Pertence a uma Layer (obrigatorio). Herda estilo visual da camada pai para renderizacao no frontend.

## Invariantes de Negocio

Geometria deve ser do mesmo tipo que o LayerType da Layer pai. Indices GiST em geometry para queries espaciais rapidas. Indice GIN em properties para queries JSONB eficientes.
