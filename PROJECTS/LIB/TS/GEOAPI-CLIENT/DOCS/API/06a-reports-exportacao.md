---
type: leaf
status: review
updated: 2026-02-07
---

# Reports API - Solicitacao de Exportacao

## Visao Geral

A Reports API fornece operacoes para geracao e download de relatorios em multiplos formatos. O acesso ocorre via o namespace api.reports no GeoApiClient. Todos os relatorios sao gerados de forma assincrona: o cliente solicita a geracao via POST, recebe um jobId, faz polling do status ate COMPLETED e entao realiza o download.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| POST | /api/reports/units/export | Solicitar exportacao de unidades |
| POST | /api/reports/holders/export | Solicitar exportacao de posseiros |
| POST | /api/reports/communities/stats | Solicitar estatisticas de comunidade |
| GET | /api/reports/:jobId/status | Verificar status de geracao |
| GET | /api/reports/:jobId/download | Download do relatorio gerado |

## Metodo exportUnits

Solicita exportacao de unidades. Recebe um objeto de filtros e o formato desejado. Retorna um ReportJob com o ID do job para acompanhamento.

### Filtros de Exportacao de Unidades

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| communityId | string | Nao | Filtrar por comunidade |
| status | UnitStatus | Nao | Filtrar por status da unidade |
| occupationType | string | Nao | RESIDENTIAL, COMMERCIAL, MIXED ou INSTITUTIONAL |
| createdAfter | Date | Nao | Unidades criadas apos esta data |
| createdBefore | Date | Nao | Unidades criadas antes desta data |
| includeHolders | boolean | Nao | Incluir dados de titulares |
| includeGeometry | boolean | Nao | Incluir coordenadas em WKT |
| includeCustomData | boolean | Nao | Incluir campos customizados |

O formato aceita os valores excel, pdf ou csv.

## Metodo exportHolders

Solicita exportacao de posseiros. Recebe um objeto de filtros e o formato desejado. Retorna um ReportJob.

### Filtros de Exportacao de Posseiros

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| communityId | string | Nao | Filtrar por comunidade |
| hasUnit | boolean | Nao | Apenas com ou sem unidade vinculada |
| createdAfter | Date | Nao | Posseiros criados apos esta data |
| createdBefore | Date | Nao | Posseiros criados antes desta data |
| includeUnits | boolean | Nao | Incluir unidades vinculadas |
| includeAddress | boolean | Nao | Incluir endereco |
| includeContact | boolean | Nao | Incluir telefone e email |
| maskCpf | boolean | Nao | Mascarar CPF no formato parcial |

## Metodo getCommunityStats

Solicita relatorio de estatisticas de uma comunidade. Recebe o communityId e o formato desejado. Retorna um ReportJob. O relatorio inclui total de unidades por status, total de posseiros, area total e media, distribuicao por tipo de ocupacao e evolucao temporal. O formato PDF inclui graficos.
