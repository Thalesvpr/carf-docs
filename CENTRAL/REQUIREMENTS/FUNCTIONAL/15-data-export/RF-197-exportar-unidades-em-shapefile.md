---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-197: Exportar Unidades em Shapefile

## Descricao

Sistema deve oferecer exportacao de unidades territoriais no formato Shapefile, padrao da industria GIS que garante interoperabilidade com softwares de geoprocessamento desktop como ArcGIS, QGIS e AutoCAD Map. Geracao cria todos os arquivos componentes obrigatorios incluindo .shp com geometrias, .shx com indice espacial, .dbf com tabela de atributos e .prj definindo sistema de coordenadas, alem de .cpg especificando encoding UTF-8. Filtros permitem segmentar unidades por comunidade, status, tipo de ocupacao, periodo ou area espacial de interesse, focando exportacao em subconjunto relevante. Dados filtrados automaticamente por tenant_id do usuario autenticado. Arquivo final empacotado em ZIP disponibilizado para download ou enviado por email.

## Criterios de Aceitacao

1. Geracao de .shp, .shx, .dbf, .prj e .cpg
2. Encoding UTF-8 para caracteres acentuados
3. Filtros por comunidade, status e periodo
4. Segregacao por tenant_id
5. Download em ZIP compactado

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-127
