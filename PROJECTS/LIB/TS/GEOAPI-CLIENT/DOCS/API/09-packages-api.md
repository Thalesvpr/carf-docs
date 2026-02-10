---
type: leaf
status: review
updated: 2026-02-08
---

# Field Packages API - Pacotes de Campo

A Packages API gerencia pacotes de dados preparados para trabalho em campo offline no REURBCAD. Pacotes contem tiles de ortofoto para as comunidades autorizadas, poligonos GeoJSON de unidades e comunidades, e metadados pre-cadastrados. Acessada via propriedade packages da instancia GeoApiClient. Endpoints conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| GET | /api/packages/field | Metadados do pacote | 200 | 403 | field-coordinator, field-cadastrator |
| GET | /api/packages/field/{id}/download | Download binario do pacote | 200 | 404 | field-coordinator, field-cadastrator |

## getFieldPackage (GET /api/packages/field)

Obtem metadados do pacote de campo disponivel para o usuario logado. O pacote e personalizado com base nas comunidades autorizadas via CommunityAuthorization conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md). Sem parametros.

Response retorna FieldPackageInfo:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| packageId | string | UUID do pacote |
| sizeBytes | number | Tamanho estimado do pacote compactado |
| communities | array de string | Nomes das comunidades incluidas |
| createdAt | string | ISO 8601 timestamp de criacao do pacote |
| downloadUrl | string | URL pre-assinada do S3 para download unico |

O pacote contem tres tipos de dados: tiles de ortofoto em formato PNG para as comunidades autorizadas do usuario (subdiretorios por comunityId e zoom level), poligonos GeoJSON de unidades e comunidades para visualizacao no mapa offline, e metadados pre-cadastrados de comunidades e unidades existentes em formato JSON para pre-popular o WatermelonDB local.

Restrito a roles field-coordinator e field-cadastrator. Retorna ForbiddenError 403 se o usuario nao tiver role adequado.

## downloadFieldPackage (GET /api/packages/field/{id}/download)

Faz download do pacote binario compactado. Aceita packageId string. Retorna Blob contendo arquivo ZIP com Content-Type application/zip. A URL pre-assinada expira apos primeiro uso para evitar compartilhamento indevido do pacote.

O REURBCAD deve salvar o Blob no sistema de arquivos local usando expo-file-system, descompactar o ZIP e alimentar o WatermelonDB com os metadados e o cache de tiles com as imagens. O processo de download deve exibir o componente Progress do @carf/ui-native com variant download para feedback visual ao usuario.

Restrito a roles field-coordinator e field-cadastrator. Lanca NotFoundError 404 se o pacote nao existir ou ja tiver sido baixado (URL expirada).
