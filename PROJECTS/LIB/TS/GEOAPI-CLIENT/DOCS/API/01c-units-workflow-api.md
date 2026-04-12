---
type: leaf
status: review
updated: 2026-02-08
---

# Units API - Workflow e Exportacao

Metodos de transicao de status e exportacao do modulo api.units conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md). Transicoes de status seguem o enum UnitStatus documentado em [04-types-enums](../../TSCORE/DOCS/API/04-types-enums.md).

## Endpoints de Workflow

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| POST | /api/units/{id}/submit | Submeter para analise | 200 | 400 NO_HOLDER | todos autenticados |
| POST | /api/units/{id}/approve | Aprovar unidade | 200 | 403 NOT_AUTHORIZED | manager+ |
| POST | /api/units/{id}/reject | Rejeitar unidade | 200 | 403 NOT_AUTHORIZED | manager+ |

## submit

O metodo submit aceita unitId string e nao requer body. Transiciona o status de DRAFT para PENDING_ANALYSIS. Pre-condicao: ao menos um titular vinculado com isPrimary true. Se nao houver titular principal, retorna ValidationError 400 com code NO_HOLDER e detail informando que a unidade precisa de pelo menos um titular principal para submissao. Retorna UnitDto com status atualizado.

## approve

O metodo approve aceita unitId string e body com justification como string obrigatoria com minimo 10 caracteres. Transiciona o status para APPROVED. Restrito a roles manager ou superior conforme hierarquia documentada em [04-types-enums](../../TSCORE/DOCS/API/04-types-enums.md). Se o usuario nao tiver permissao, retorna ForbiddenError 403 com code NOT_AUTHORIZED. Retorna UnitDto atualizado.

## reject

O metodo reject aceita unitId string e body com reason como string obrigatoria com minimo 50 caracteres. Transiciona o status para REJECTED. Restrito a roles manager ou superior. O motivo da rejeicao e registrado para que o cadastrador possa entender o que precisa ser corrigido. Retorna UnitDto atualizado.

## Endpoints de Exportacao

| Metodo HTTP | Rota | Descricao | Sucesso | Roles |
|:------------|:-----|:----------|:--------|:------|
| GET | /api/units/geojson | Exportar como GeoJSON | 200 | todos autenticados |

## exportGeoJson

O metodo exportGeoJson aceita ListUnitsQueryDTO opcional para filtrar quais unidades incluir e retorna Promise de GeoJSON FeatureCollection. Cada unidade com boundary definido e representada como Feature com geometry do tipo Polygon e properties contendo id, code, status e attendanceStatus. Unidades sem boundary sao incluidas como Feature com geometry null. O resultado e diretamente compativel com bibliotecas de mapeamento como Leaflet, Mapbox GL JS e react-native-maps para visualizacao espacial.
