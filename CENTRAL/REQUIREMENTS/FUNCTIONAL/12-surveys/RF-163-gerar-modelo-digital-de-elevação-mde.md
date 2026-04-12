---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-163: Gerar Modelo Digital de Elevacao (MDE)

## Descricao

Sistema deve gerar Modelo Digital de Elevacao atraves de interpolacao de grid regular a partir de pontos topograficos, criando representacao matricial continua do terreno onde cada pixel armazena valor de altitude interpolado. Processamento utiliza tecnicas geoestalisticas para distribuir espacialmente valores de elevacao. MDE exportado em formato GeoTIFF padrao OGC incluindo metadados de georreferenciamento e sistema de coordenadas, garantindo interoperabilidade com softwares GIS externos para analises avancadas (declividade, orientacao de vertentes, sombreamento). Visualizacao do MDE como camada raster sobreposta ao mapa base com esquemas de cores hipsometricos para interpretacao visual do relevo.

## Criterios de Aceitacao

1. Interpolacao de grid regular
2. Exportacao em GeoTIFF
3. Metadados de georreferenciamento
4. Visualizacao como camada raster
5. Esquema de cores hipsometrico

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-162
