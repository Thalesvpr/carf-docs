---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-034: Criar Comunidade

## Descricao

Usuarios com role ADMIN podem criar novas comunidades no tenant. Formulario inclui campos obrigatorios nome descritivo, tipo de comunidade (selecionado de enum predefinido), municipio e estado atraves de dropdowns hierarquicos, populacao estimada e area aproximada. Geometria (poligono) opcional podendo ser definida posteriormente ou desenhada diretamente no mapa interativo. Upload de shapefile ou KML como alternativa ao desenho manual, parseado e convertido para GeoJSON.

## Criterios de Aceitacao

1. Formulario com campos obrigatorios nome, tipo, municipio e estado
2. Desenho de poligono no mapa com ferramentas interativas
3. Upload de shapefile ou KML com validacao geometrica
4. Conversao automatica para GeoJSON e armazenamento PostGIS
5. Validacao topologica garantindo poligono fechado e valido

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-039, RF-040
