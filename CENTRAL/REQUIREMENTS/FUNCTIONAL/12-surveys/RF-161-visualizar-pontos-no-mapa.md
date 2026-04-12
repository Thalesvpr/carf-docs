---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-161: Visualizar Pontos no Mapa

## Descricao

Sistema deve renderizar pontos topograficos importados no mapa interativo atraves de marcadores visuais que exibem codigo identificador de cada ponto, permitindo localizar e identificar vertices do levantamento cadastral. Ao clicar em marcadores, popup exibe informacoes detalhadas incluindo coordenadas planas (X, Y), altitude (Z) e metadados associados, facilitando verificacao e validacao sem consultar arquivo original. Pontos organizados em camada dedicada independente das demais features, possibilitando controle granular de visibilidade (ativar/desativar). Separacao em camadas otimiza desempenho ao trabalhar com grandes volumes de pontos, garantindo fluidez na navegacao em projetos cadastrais extensos com milhares de coordenadas.

## Criterios de Aceitacao

1. Marcadores com codigo identificador
2. Popup com coordenadas X, Y, Z
3. Camada dedicada para pontos
4. Toggle de visibilidade
5. Performance com grandes volumes

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-160, RF-151
