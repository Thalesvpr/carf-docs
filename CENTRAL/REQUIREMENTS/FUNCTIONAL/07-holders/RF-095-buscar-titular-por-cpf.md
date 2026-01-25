---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-095: Buscar Titular por CPF

## Descricao

Sistema deve oferecer busca rapida de titulares por CPF ou CNPJ com autocomplete em tempo real enquanto usuario digita. Busca normaliza entrada removendo formatacao antes de consultar garantindo encontrar titular independente de como usuario digita. Quando multiplos titulares com mesmo documento sao encontrados, sistema alerta sobre duplicacao e oferece mesclagem. Interface de formulario de unidade integra busca com autocomplete para vinculacao rapida de titulares existentes.

## Criterios de Aceitacao

1. Autocomplete em tempo real por documento
2. Normalizacao de entrada (remove formatacao)
3. Alerta de duplicatas encontradas
4. Integracao com formulario de unidade
5. Opcao de criar novo se nao encontrado

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-084, RF-061
