---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-067: Importar Unidades via Shapefile

## Descricao

Sistema deve permitir que usuarios ADMIN importem multiplas unidades atraves de upload de arquivo shapefile (.zip contendo .shp, .shx, .dbf, .prj). Interface GEOWEB oferece wizard guiando processo de importacao em etapas. Wizard de mapeamento permite associar colunas do shapefile aos campos do modelo de unidade com sugestoes automaticas baseadas em nomes similares. Preview mostra estatisticas e alertas sobre problemas antes do commit. Importacao transacional garante consistencia com rollback em caso de falha.

## Criterios de Aceitacao

1. Upload de shapefile compactado (.zip)
2. Wizard de mapeamento de campos
3. Preview com estatisticas e validacoes
4. Importacao transacional com rollback
5. Restrito a perfil ADMIN

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-066
