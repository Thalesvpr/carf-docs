---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-109: Tipos de Foto

## Descricao

Sistema deve suportar categorizacao de fotos atraves de tipos predefinidos: FACHADA (fotos externas frontais), INTERIOR (ambientes internos), TERRENO (areas sem construcao), DOCUMENTOS (fotografias de papeis), OUTRO (casos nao enquadrados). Implementacao via enum no campo photo_type. Tipo obrigatorio no momento do upload ou atribuido posteriormente. Filtros por tipo em listagem e galeria permitem visualizacao por categoria especifica. Queries eficientes por tipo atraves de indices.

## Criterios de Aceitacao

1. Enum: FACHADA, INTERIOR, TERRENO, DOCUMENTOS, OUTRO
2. Campo photo_type obrigatorio ou editavel
3. Filtros por tipo em galeria
4. Descricoes claras de cada tipo
5. Indices para queries por tipo

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-108, RF-063
