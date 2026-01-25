---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - REURBCAD
---

# RF-110: Geotagging de Fotos

## Descricao

Sistema deve automaticamente extrair e armazenar coordenadas geograficas de fotos que contenham metadados EXIF com GPS. Extracao de latitude e longitude durante upload com validacao de formato e range. Coordenadas armazenadas como geometria Point no PostGIS permitindo queries espaciais. Fotos sem dados GPS no EXIF permanecem com campo nulo sem rejeitar upload, permitindo atribuicao manual posterior. Particularmente valioso para fotos capturadas via REURBCAD mobile com GPS habilitado conforme WORKFLOW-MESTRE.

## Criterios de Aceitacao

1. Extracao automatica de GPS do EXIF
2. Armazenamento como Point no PostGIS
3. Validacao de formato e range
4. Campo nulo se sem GPS (nao rejeita)
5. Suporte a atribuicao manual

## Rastreabilidade

- Modulos: GEOAPI, REURBCAD
- Requisitos dependentes: RF-108, RF-117
