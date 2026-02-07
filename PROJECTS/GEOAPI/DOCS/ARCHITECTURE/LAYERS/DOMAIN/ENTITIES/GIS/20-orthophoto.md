---
type: leaf
status: approved
updated: 2026-02-07
---

# Orthophoto

Entidade representando uma ortofoto georreferenciada de drone vinculada a um tenant e opcionalmente a uma comunidade especifica. Armazena metadados do arquivo original, versao otimizada para web e piramide de tiles gerada pelo pipeline de processamento GDAL. O ciclo de vida acompanha o processamento assincrono: upload inicial marca status PENDING, processamento via Hangfire muda para PROCESSING, e conclusao bem-sucedida ou falha marca COMPLETED ou FAILED respectivamente.

## Papel no Dominio

Ortofotos sao a base visual do sistema de campo: servidas como tiles XYZ no mapa do REURBCAD mobile e no GeoWeb, permitindo que equipes de campo e analistas visualizem a situacao real do terreno com alta resolucao. O upload e feito por analistas via GEOAPI, o processamento gera tiles otimizados, e o pacote de campo inclui os tiles relevantes para download offline. Sem ortofoto processada, a equipe de campo opera apenas com mapa base generico.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | FK para Tenant. Municipio proprietario da ortofoto. |
| CommunityId | Guid | sim | FK para Community. Nullable quando a ortofoto cobre area mais ampla que uma comunidade. |
| OriginalPath | string | nao | Caminho no bucket S3 do arquivo original (tipicamente GeoTIFF). Formato: {tenant_id}/orthofotos/{id}/original. |
| OptimizedPath | string | sim | Caminho S3 da versao otimizada para web (JPEG quality 85, lado maior limitado a 4096px). Preenchido apos processamento. |
| TilesPath | string | sim | Caminho base S3 da piramide de tiles XYZ (formato: {tenant_id}/orthofotos/{id}/tiles/{z}/{x}/{y}.png). Preenchido apos processamento. |
| FileSize | long | nao | Tamanho do arquivo original em bytes. |
| Width | int | sim | Largura em pixels. Extraida via GDAL durante processamento. |
| Height | int | sim | Altura em pixels. Extraida via GDAL durante processamento. |
| Srid | int | sim | Sistema de referencia espacial (tipicamente 4326 WGS84). Extraido via GDAL. |
| BoundsGeoJson | string | sim | Limites geograficos da ortofoto em formato GeoJSON armazenado como JSONB. Extraido via GDAL. |
| CaptureDate | DateOnly | sim | Data da captura aerea pelo drone. Informada pelo uploader. |
| ProcessingStatus | string | nao | Status do processamento: PENDING (aguardando), PROCESSING (em andamento), COMPLETED (concluido), FAILED (falhou). |
| ProcessingError | string | sim | Mensagem de erro quando status e FAILED. Contem descricao especifica do problema (arquivo sem georreferenciamento, formato invalido, erro GDAL). |
| UploadedAt | DateTime | nao | Momento do upload. |
| UploadedBy | Guid | nao | ID do usuario que fez upload. |
| ProcessedAt | DateTime | sim | Momento da conclusao do processamento (sucesso ou falha). |

## Relacionamentos

Pertence a um Tenant via TenantId. Opcionalmente vinculada a uma Community via CommunityId.

Nao possui relacionamento direto com outras entidades. E consumida indiretamente: o pacote de campo inclui tiles de ortofotos do tenant, e o mapa do REURBCAD e GeoWeb renderiza os tiles via endpoint de tiles da GEOAPI.

## Invariantes de Negocio

ProcessingStatus deve seguir transicoes validas: PENDING so pode ir para PROCESSING, PROCESSING pode ir para COMPLETED ou FAILED. Nao ha retorno de COMPLETED ou FAILED para estados anteriores; em caso de reprocessamento, um novo registro e criado.

OriginalPath deve ser preenchido no momento da criacao. OptimizedPath e TilesPath sao preenchidos apenas pelo job de processamento, nunca pelo usuario.

FileSize deve ser positivo e nao pode exceder o limite configurado (default 2GB para ortofotos GeoTIFF).

Quando ProcessingStatus e FAILED, ProcessingError deve estar preenchido. Quando ProcessingStatus e COMPLETED, Width, Height, Srid e BoundsGeoJson devem estar preenchidos.

Ortofoto so pode ser excluida se ProcessingStatus for PENDING ou FAILED. Ortofotos COMPLETED que ja foram incluidas em pacotes de campo nao devem ser excluidas sem validacao adicional.

## Domain Events

OrthophotoUploadedEvent emitido apos upload bem-sucedido, disparando o job Hangfire de processamento. OrthophotoProcessedEvent emitido quando processamento completa com sucesso, permitindo notificacao ao uploader e atualizacao de pacotes de campo. OrthophotoFailedEvent emitido quando processamento falha, notificando o uploader com a mensagem de erro.
