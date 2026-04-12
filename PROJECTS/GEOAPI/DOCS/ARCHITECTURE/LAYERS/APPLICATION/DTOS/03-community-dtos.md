---
type: leaf
status: review
updated: 2026-02-08
---

# Community DTOs

Os Data Transfer Objects de comunidades definem os contratos de entrada e saida da API para operacoes sobre o agregado Community.

## DTOs de Resposta

CommunityDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| Code | string | Codigo unico por tenant |
| Name | string | Nome da comunidade |
| CommunityType | string | URBANA, RURAL, QUILOMBOLA, RIBEIRINHA |
| Boundary | GeometryDto | Poligono GeoJSON (nullable) |
| AreaM2 | decimal | Area em metros quadrados (nullable) |
| Municipality | string | Municipio |
| State | string | UF |
| District | string | Distrito (nullable) |
| Neighborhood | string | Bairro (nullable) |
| Reference | string | Referencia (nullable) |
| Status | string | Status da comunidade |
| UnitsCount | int | Quantidade de unidades (opcional) |
| CreatedAt | DateTime | Data de criacao |
| UpdatedAt | DateTime | Ultima atualizacao |

CommunityListItemDto e o DTO reduzido para listagens contendo Id, Code, Name, CommunityType, UnitsCount e AreaM2.

CommunitySummaryDto e o DTO minimo usado em contextos de vinculacao com unidades, contendo Id, Code e Name.

## DTOs de Request

CreateCommunityRequest contem code (obrigatorio), name (obrigatorio), communityType (obrigatorio), boundary (GeoJSON Polygon opcional), municipality (obrigatorio), state (obrigatorio, 2 letras), district (opcional), neighborhood (opcional) e reference (opcional).

UpdateCommunityRequest contem name, boundary, district, neighborhood e reference, todos opcionais para atualizacao parcial. Code e communityType nao podem ser alterados.
