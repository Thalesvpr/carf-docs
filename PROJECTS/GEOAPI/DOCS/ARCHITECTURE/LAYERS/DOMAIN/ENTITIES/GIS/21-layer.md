---
type: leaf
status: approved
updated: 2026-02-07
---

# Layer

Entidade representando camada GIS customizavel por tenant para visualizacao de dados espaciais adicionais no mapa. Exemplos de uso incluem areas de risco, redes de infraestrutura, perimetros de preservacao ambiental e zoneamento urbano. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

Layers permitem que cada municipio adicione informacoes espaciais relevantes para seu contexto sem alterar o schema do banco. O analista importa dados GIS (Shapefiles, GeoJSON) que sao convertidos em LayerFeatures, e o frontend renderiza essas camadas sobre o mapa base com estilo configuravel.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| Name | string | nao | Nome da camada. Exemplos: "Areas de Risco", "Rede de Agua", "Zoneamento". |
| LayerType | string | nao | Tipo de geometria permitida nas features: POINT, LINESTRING, POLYGON. |
| SourceUrl | string | sim | URL de origem se importada de servico externo (WMS, WFS). |
| Visible | bool | nao | Visivel por padrao no mapa. Default true. |
| Opacity | decimal | nao | Opacidade de 0.00 (transparente) a 1.00 (opaco). Default 1.00. |
| ZIndex | int | nao | Ordem de empilhamento. Camada com maior ZIndex fica por cima. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Colecao de LayerFeatures contendo as geometrias individuais da camada. Todas as features devem ter geometria compativel com o LayerType da camada pai.

## Invariantes de Negocio

LayerType restringe o tipo de geometria das features filhas. Tentativa de adicionar feature com tipo incompativel gera erro de validacao. Opacity deve estar entre 0 e 1.
