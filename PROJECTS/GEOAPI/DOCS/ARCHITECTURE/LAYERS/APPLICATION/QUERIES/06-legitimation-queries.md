---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation Queries

As queries de legitimacao implementam o lado de leitura do CQRS para o agregado LegitimationRequest, incluindo consulta de processos, historico de respostas e download de certidoes.

## GetLegitimationByIdQuery

Recebe Id do processo como Guid. O handler carrega o registro com eager loading de respostas (legitimation_responses) e certidoes (legitimation_certificates). Retorna LegitimationRequestDto completo com status atual, prazos, dados da unidade e titular vinculados, historico de respostas e informacoes da certidao quando emitida. Retorna 404 se nao encontrado.

## ListLegitimationRequestsQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina (maximo 100) |
| Status | string | nulo | Filtro por status do processo |
| UnitId | Guid | nulo | Filtro por unidade |
| SortBy | string | requested_at | Campo de ordenacao |
| SortDir | string | desc | Direcao |

Retorna PaginatedResult de LegitimationListItemDto contendo id, unitCode, holderName, status, requestedAt, deadline e analystName.

## GetLegitimationCertificateQuery

Recebe RequestId como Guid. O handler verifica que o processo tem status TITLE_ISSUED ou REGISTERED. Carrega o registro de legitimation_certificates e retorna stream do arquivo PDF armazenado no S3. O controller serve o arquivo com Content-Type application/pdf e Content-Disposition attachment com o certificate_number no nome do arquivo. Retorna 404 se o processo nao existe ou se nao tem certidao emitida.
