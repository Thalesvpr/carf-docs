---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-135: Listar Features

## Descricao

Sistema deve fornecer endpoint e interface para listar features de uma camada especifica permitindo navegacao e gerenciamento dos elementos geograficos cadastrados. Filtro por camada como parametro obrigatorio garante que apenas features da layer selecionada sejam exibidas, evitando mistura de dados de diferentes camadas com schemas distintos. Paginacao robusta para camadas com grande volume divide resultados em paginas de tamanho configuravel (20 a 100 registros) com metadados de total de registros, pagina atual e total de paginas. Busca por atributos permite filtrar features baseado em valores de propriedades customizadas via queries JSON sobre campo properties. Listagem pode incluir representacao simplificada da geometria como centroide ou bbox para features complexas.

## Criterios de Aceitacao

1. Filtro obrigatorio por camada
2. Paginacao com metadados
3. Busca por atributos customizados
4. Representacao simplificada de geometria
5. Ordenacao configuravel

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-132, RF-136
