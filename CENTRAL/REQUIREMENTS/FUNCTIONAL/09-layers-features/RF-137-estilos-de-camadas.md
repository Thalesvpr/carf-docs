---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-137: Estilos de Camadas

## Descricao

Sistema deve suportar configuracao detalhada de estilos visuais de camadas GIS controlando como features sao renderizadas no mapa, permitindo diferenciacao visual entre layers. Configuracoes incluem fill color (cor de preenchimento para poligonos via seletor ou codigo hexadecimal), stroke color (cor de bordas de poligonos e linhas), e stroke width (espessura em pixels). Controle de opacidade configuravel para fill e stroke permite criar overlays semitransparentes que revelam camadas subjacentes, util para analises com multiplas informacoes sobrepostas. Para camadas de pontos, sistema permite selecao de icones de biblioteca predefinida ou upload de icones customizados, renderizados como marcadores em tamanho configuravel. Estilos armazenados como JSON no modelo da camada e aplicados consistentemente em toda renderizacao.

## Criterios de Aceitacao

1. Configuracao de fill color e stroke color
2. Configuracao de stroke width
3. Controle de opacidade
4. Selecao de icones para camadas de pontos
5. Armazenamento de estilos como JSON

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-128
