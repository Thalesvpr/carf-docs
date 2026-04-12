---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-170: Integracao com GNSS

## Descricao

Sistema deve importar dados coletados por receptores GNSS/GPS atraves de parsers para formatos padrao da industria: RINEX para dados brutos de observacao satelital e NMEA 0183 para sentencas de posicionamento em tempo real. Opcionalmente implementa processamento de correcao diferencial usando dados de estacoes de referencia para refinar coordenadas, melhorando precisao de nivel metrico para submétrico ou centimetrico conforme metodo (pos-processado ou RTK). Apos importacao e processamento, sistema cria pontos georreferenciados associando metadados de qualidade (PDOP, numero de satelites, tipo de solucao) permitindo rastreabilidade da precisao esperada para cada vertice. Fundamental para conformidade com requisitos INCRA para certificacao de imoveis rurais e urbanos.

## Criterios de Aceitacao

1. Parsers para RINEX e NMEA 0183
2. Correcao diferencial opcional
3. Metadados de qualidade (PDOP, satelites)
4. Criacao de pontos georreferenciados
5. Rastreabilidade de precisao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-157
