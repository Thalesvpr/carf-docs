---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-165: Ajustar Sistema de Coordenadas

## Descricao

Sistema deve permitir configurar SRID (Spatial Reference Identifier) do levantamento topografico, selecionando sistema de referencia espacial atraves de codigos EPSG padronizados (projecao cartografica, datum geodesico, zona UTM). Ao alterar SRID, sistema executa automaticamente reprojecao de todas coordenadas dos pontos utilizando transformacoes geodesicas precisas, garantindo consistencia espacial entre dados coletados em diferentes sistemas e integracao com bases cartograficas oficiais. Validacao verifica coerencia das coordenadas apos transformacao, identificando inconsistencias resultantes de erros de parametrizacao ou sistemas incompativeis, alertando usuario antes de persistir. Critico em projetos cadastrais brasileiros onde coexistem dados em SIRGAS2000 UTM, Corrego Alegre e sistemas locais arbitrarios.

## Criterios de Aceitacao

1. Selecao de SRID via codigo EPSG
2. Reprojecao automatica de coordenadas
3. Transformacoes geodesicas precisas
4. Validacao de coerencia apos transformacao
5. Alerta de inconsistencias

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-157
