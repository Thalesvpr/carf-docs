---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-150: Zoom para Camada

## Descricao

Sistema deve permitir acionar zoom automatico para extent completo de uma camada especifica, navegando rapidamente para visualizacao de todas as features contidas independente de localizacao atual do mapa. Sistema calcula bbox da camada atraves de query espacial determinando extensao minima e maxima que engloba todas as features nao excluidas, utilizando funcoes PostGIS como ST_Extent ou agregacao de ST_Envelope. Apos calcular bbox, sistema executa zoom com padding adequado (tipicamente 10% a 20% da dimensao) garantindo que features nas bordas nao fiquem coladas as extremidades do viewport. Transicao de zoom inclui animacao suave (500ms a 1000ms) interpolando entre viewport atual e destino para manter orientacao espacial. Funcionalidade acionada via botao ou opcao de menu no item da camada no painel.

## Criterios de Aceitacao

1. Calculo de bbox via ST_Extent
2. Padding ao redor do extent
3. Animacao suave de transicao
4. Botao ou menu no painel de camadas
5. Funciona com qualquer quantidade de features

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-130
