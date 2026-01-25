---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-136: Atributos Customizados de Features

## Descricao

Sistema deve suportar conjunto flexivel de atributos customizados definidos por camada ao inves de schema rigido pre-determinado, com propriedades armazenadas em estrutura JSON permitindo extensibilidade sem alteracoes de schema de banco. Campo properties do tipo JSONB no PostgreSQL armazena objeto JSON com pares chave-valor, permitindo indexacao eficiente, queries sobre propriedades individuais e validacao de estrutura. Cada camada pode definir schema de atributos configuravel especificando campos disponiveis com nome, tipo de dado (texto, numero, data, booleano, enum) e obrigatoriedade, permitindo customizacao conforme dominio sem programacao. Sistema valida tipos ao criar ou editar features, rejeitando submissoes com tipos incorretos ou campos obrigatorios ausentes. Interface gera formularios dinamicos baseados no schema configurado.

## Criterios de Aceitacao

1. Campo properties JSONB no PostgreSQL
2. Schema de atributos configuravel por camada
3. Tipos suportados: texto, numero, data, booleano, enum
4. Validacao de tipos e obrigatoriedade
5. Formularios dinamicos baseados no schema

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-127, RF-132
