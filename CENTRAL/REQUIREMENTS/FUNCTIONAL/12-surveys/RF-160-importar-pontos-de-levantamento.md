---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-160: Importar Pontos de Levantamento

## Descricao

Sistema deve permitir importacao de coordenadas de pontos topograficos atraves de arquivos CSV ou TXT contendo dados geodesicos coletados em campo (coordenadas X, Y, Z e codigos de identificacao). Mapeamento de colunas permite correlacionar campos do arquivo importado com atributos esperados pelo sistema, garantindo flexibilidade para diferentes estruturas de dados de equipamentos diversos. Apos processamento, sistema cria automaticamente features do tipo Point no banco geoespacial PostGIS permitindo visualizacao e analise posterior. Integracao com unidades territoriais e comunidades existentes conforme segregacao por tenant. Essencial para projetos de regularizacao fundiaria que demandam levantamentos de precisao.

## Criterios de Aceitacao

1. Upload de arquivos CSV e TXT
2. Mapeamento de colunas configuravel
3. Criacao de features Point em PostGIS
4. Validacao de coordenadas
5. Integracao com unidades e comunidades

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-157, RF-132
