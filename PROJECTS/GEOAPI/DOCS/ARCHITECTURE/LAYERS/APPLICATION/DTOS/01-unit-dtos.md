---
type: leaf
status: active
updated: 2026-02-07
---

# Unit DTOs

Os Data Transfer Objects de unidades habitacionais definem os contratos de entrada e saida da API. Todos sao implementados como records imutaveis.

## DTOs de Resposta

UnitDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| Code | string | Codigo no formato UNI-YYYY-NNNNN |
| Status | string | Estado atual da unidade |
| Address | AddressDto | Endereco completo |
| Geometry | GeometryDto | Poligono GeoJSON |
| AreaM2 | decimal | Area calculada em metros quadrados |
| Centroid | CentroidDto | Centroide do poligono |
| Photos | lista de PhotoDto | Fotos da unidade (opcional) |
| Holders | lista de HolderSummaryDto | Titulares vinculados (opcional) |
| Community | CommunitySummaryDto | Comunidade associada (opcional) |
| TenantId | Guid | Identificador do tenant |
| CreatedAt | DateTime | Data de criacao |
| UpdatedAt | DateTime | Data de atualizacao |

UnitSummaryDto e o DTO reduzido utilizado em listagens, contendo Id, Code, Status, FullAddress (endereco formatado), AreaM2, Centroid, HoldersCount e CreatedAt.

## DTOs de Request

CreateUnitRequest contem Address (obrigatorio), Geometry (obrigatorio), CommunityId (opcional), Photos (opcional) e Metadata (dicionario opcional de metadados). UpdateUnitRequest contem Address (opcional), Geometry (opcional) e Photos (opcional), permitindo atualizacao parcial.

## DTOs Auxiliares

AddressDto contem Street, Number, Complement (opcional), Neighborhood, City, State e ZipCode. Possui propriedade calculada FullAddress que formata o endereco completo concatenando logradouro, numero, complemento quando presente, bairro, cidade e UF. GeometryDto contem Type (sempre "Polygon") e Coordinates (array tridimensional de doubles representando aneis de coordenadas GeoJSON). CentroidDto contem Latitude e Longitude como doubles.
