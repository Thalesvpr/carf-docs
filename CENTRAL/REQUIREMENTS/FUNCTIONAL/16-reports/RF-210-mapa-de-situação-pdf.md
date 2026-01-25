---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-210: Mapa de Situacao PDF

## Descricao

Sistema deve possibilitar geracao automatizada de Mapa de Situacao em formato PDF apresentando representacao cartografica estatica de unidade territorial ou comunidade, produzindo documento tecnico para anexacao a processos administrativos ou documentacao formal. Renderizacao implementa composicao cartografica apropriada incluindo feature destacada sobre basemap contextual, escala grafica e numerica, seta indicadora de norte geografico, e legenda explicativa. PDF segue padroes cartograficos tecnicos com grid de coordenadas, texto de projecao e datum, referencia a fonte de dados e cabecalho institucional. Customizacao de parametros inclui escala, extensao espacial, camadas adicionais e formato de pagina (A4, A3, oficio).

## Criterios de Aceitacao

1. Composicao cartografica completa
2. Escala grafica e numerica
3. Norte geografico e legenda
4. Grid de coordenadas e projecao
5. Formatos de pagina configuraveis

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-044
