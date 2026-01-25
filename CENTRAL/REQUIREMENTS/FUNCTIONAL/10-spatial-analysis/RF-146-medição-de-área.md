---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
---

# RF-146: Medicao de Area

## Descricao

Sistema deve fornecer ferramenta interativa de medicao de area permitindo calcular superficie de poligonos desenhados diretamente no mapa para analise de extensoes territoriais sem criar features permanentes. Interface permite ativar modo de medicao e desenhar poligono atraves de cliques sequenciais marcando vertices do perimetro, onde ultimo clique fecha poligono automaticamente ou via double-click, calculando imediatamente area da superficie delimitada. Area calculada em metros quadrados como unidade base com conversao para hectares quando excede 10000 m2. Exibicao formatada com separadores de milhares e casas decimais adequadas. Ferramenta inclui opcao de limpeza para nova medicao. Calculo considera geometria geodesica da Terra para precisao usando funcoes como ST_Area com tipo geography do PostGIS ou calculos equivalentes no cliente.

## Criterios de Aceitacao

1. Desenho de poligono via cliques sequenciais
2. Calculo automatico de area
3. Unidades adaptativas (m2/hectares)
4. Formatacao legivel de valores
5. Calculo geodesico para precisao

## Rastreabilidade

- Modulos: GEOWEB
- Requisitos dependentes: RF-053
