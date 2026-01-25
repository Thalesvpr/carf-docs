---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-063: Anexar Fotos a Unidade

## Descricao

Sistema deve permitir upload multiplo de fotografias relacionadas a unidades habitacionais. Cada foto pode ser categorizada por tipo (FACHADA, INTERIOR, DOCUMENTOS, SITUACAO_IRREGULAR, OUTRO). Upload suporta selecao multipla de arquivos com validacao de formato (JPG, PNG, HEIC) e tamanho maximo por arquivo. Sistema gera automaticamente thumbnails otimizadas para exibicao rapida. Metadados de geotagging capturados quando disponiveis.

## Criterios de Aceitacao

1. Upload multiplo de fotos com categorizacao
2. Validacao de formato e tamanho maximo
3. Geracao automatica de thumbnails
4. Captura de metadados de geotagging
5. Galeria com visualizacao e exclusao

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-049
