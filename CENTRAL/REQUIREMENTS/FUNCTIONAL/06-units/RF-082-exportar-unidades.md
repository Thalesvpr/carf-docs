---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-082: Exportar Unidades

## Descricao

Sistema deve permitir exportacao de unidades selecionadas ou filtradas em multiplos formatos (SHAPEFILE, KML, GEOJSON, CSV, EXCEL) atendendo diferentes casos de uso. Exportacao respeita filtros ativos garantindo que apenas unidades visiveis sejam incluidas. Interface oferece opcao de incluir fotos e documentos anexados gerando arquivo ZIP com dados principais e pasta de anexos organizados por codigo. Suporta intercambio com stakeholders externos, backup e integracao com sistemas legados.

## Criterios de Aceitacao

1. Formatos: Shapefile, KML, GeoJSON, CSV, Excel
2. Exportacao respeitando filtros ativos
3. Opcao de incluir anexos
4. Geracao de ZIP com anexos organizados
5. Download de arquivo exportado

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-052
