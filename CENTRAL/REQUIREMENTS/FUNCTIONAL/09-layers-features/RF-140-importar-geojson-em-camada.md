---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-140: Importar GeoJSON em Camada

## Descricao

Sistema deve permitir importacao de arquivos GeoJSON em camadas existentes para ingestao de dados geoespaciais de fonte externa ou sistema terceiro. Upload aceita arquivo .geojson validando que conteudo e JSON bem-formado e estrutura corresponde a especificacao GeoJSON com FeatureCollection contendo array de Features. Validacao de estrutura verifica presenca de campos obrigatorios (type, geometry, properties) em cada feature, validade das geometrias conforme especificacao, e compatibilidade de tipos de geometria com tipo configurado na camada destino. Processamento itera sobre array extraindo geometria, convertendo para formato PostGIS e mapeando properties para atributos customizados conforme schema da camada. Importacao ocorre em transacao unica permitindo rollback completo se qualquer feature falhar. Sistema fornece feedback de progresso e relatorio final.

## Criterios de Aceitacao

1. Upload de arquivo .geojson
2. Validacao de estrutura GeoJSON
3. Verificacao de compatibilidade de geometria
4. Mapeamento de properties para atributos
5. Transacao unica com rollback

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-132, RF-136
