---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-115: Geracao de Miniaturas

## Descricao

Sistema deve gerar automaticamente miniaturas de fotos no momento do upload para otimizar performance em galerias. Dimensoes de 200x200 pixels em formato quadrado com crop inteligente centralizando area de interesse ou preenchimento para consistencia visual em grids. Geracao automatica no pipeline de upload junto com compressao e extracao EXIF. Armazenamento separado em S3/MinIO com prefixo ou bucket diferente permitindo politicas de cache especificas. API retorna URLs separadas para original e thumbnail.

## Criterios de Aceitacao

1. Dimensoes 200x200 pixels quadrado
2. Crop inteligente ou preenchimento
3. Geracao automatica no upload
4. Armazenamento separado de originais
5. URLs distintas para original e thumbnail

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-108, RF-111, RF-116
