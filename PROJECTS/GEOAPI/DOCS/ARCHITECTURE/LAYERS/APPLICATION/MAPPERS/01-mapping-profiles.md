---
type: leaf
status: review
updated: 2026-02-08
---

# Mapping Profiles

Os profiles do AutoMapper configuram o mapeamento bidirecional entre entidades de dominio e DTOs na GEOAPI. Sao registrados automaticamente no DI por assembly scanning a partir do assembly que contem UnitMappingProfile.

## UnitMappingProfile

Configura tres mapeamentos. De Unit para UnitDto: converte a propriedade Boundary para GeometryDto em formato GeoJSON, converte Centroid para CentroidDto (invertendo X/Y para latitude/longitude) e projeta os holders a partir da colecao UnitHolders. De Unit para UnitSummaryDto: mapeia FullAddress a partir do value object Address e HoldersCount a partir da contagem de UnitHolders. Adicionalmente, configura mapeamentos reversos de AddressDto para Address e de GeometryDto para Geometry (este ultimo via GeometryConverter customizado).

## HolderMappingProfile

Configura dois mapeamentos. De Holder para HolderDto: mapeia CpfMasked a partir da propriedade Masked do value object CPF e calcula Age a partir da data de nascimento. De Holder para HolderSummaryDto: mapeamento direto por convencao de nomes. De Holder para HolderListItemDto: projeta Id, CpfMasked, FullName, BirthDate, Gender e calcula UnitsCount a partir da contagem de UnitHolders associados.

## CommunityMappingProfile

Configura tres mapeamentos. De Community para CommunityDto: converte Boundary para GeometryDto em formato GeoJSON e calcula UnitsCount quando solicitado via projecao. De Community para CommunityListItemDto: mapeia Code, Name, CommunityType, AreaM2 e UnitsCount. De Community para CommunitySummaryDto: mapeamento direto de Id, Code e Name.

## LegitimationMappingProfile

Configura dois mapeamentos. De LegitimationRequest para LegitimationRequestDto: projeta dados da unidade e titular principal via navegacao de relacionamentos, inclui lista de LegitimationResponse mapeadas para ResponseDto e LegitimationCertificate mapeada para CertificateDto quando existente. De LegitimationRequest para LegitimationListItemDto: projeta UnitCode via Unit.Code, HolderName via navegacao por UnitHolders e AnalystName via lookup.

## DocumentMappingProfile

Configura dois mapeamentos. De Document para DocumentDto: mapeamento direto por convencao de nomes sem transformacoes especiais. De Document para DocumentListItemDto: subconjunto com Id, FileName, FileSize, MimeType, DocumentType e UploadedAt.

## OrtofotoMappingProfile

Configura dois mapeamentos. De Ortofoto para OrtofotoDto: converte BoundsGeoJson de JSONB para objeto GeoJSON. De Ortofoto para OrtofotoListItemDto: subconjunto com Id, CommunityId, CaptureDate, FileSize, ProcessingStatus e UploadedAt.

## GeometryConverter

Implementa ITypeConverter para converter GeometryDto em Geometry do NetTopologySuite. Extrai o array de coordenadas do anel externo do poligono, cria objetos Coordinate a partir de cada par longitude/latitude e utiliza o GeometryFactory para construir o poligono.

## Mapeamentos Resumidos

| Origem | Destino | Transformacoes Especiais |
|--------|---------|-------------------------|
| Unit | UnitDto | Boundary para GeoJSON, Centroid para lat/lng, Holders projetados |
| Unit | UnitSummaryDto | FullAddress formatado, HoldersCount calculado |
| Holder | HolderDto | CPF mascarado, idade calculada |
| Holder | HolderListItemDto | CPF mascarado, UnitsCount calculado |
| Community | CommunityDto | Boundary para GeoJSON, UnitsCount opcional |
| Community | CommunityListItemDto | AreaM2, UnitsCount |
| LegitimationRequest | LegitimationRequestDto | Unit e Holder projetados, Responses e Certificate incluidos |
| Document | DocumentDto | Mapeamento direto |
| Ortofoto | OrtofotoDto | BoundsGeoJson convertido |
| AddressDto | Address | Mapeamento direto |
| GeometryDto | Geometry | Conversao via GeometryConverter |
