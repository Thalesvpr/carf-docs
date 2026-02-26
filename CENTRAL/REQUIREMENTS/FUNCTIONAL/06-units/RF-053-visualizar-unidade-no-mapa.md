---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - REURBCAD
---

# RF-053: Visualizar Unidade no Mapa

## Descricao

Sistema deve exibir unidade no mapa web interativo com geometria colorida por status de workflow. Renderizacao de poligono com cores por status: DRAFT em cinza, PENDING em laranja, APPROVED em verde, REJECTED em vermelho, CHANGES_REQUESTED em azul. Popup ou painel lateral exibindo dados resumidos ao clicar em poligono incluindo codigo, endereco, tipo, area, titulares, status e acoes rapidas. Performance otimizada para grandes quantidades de features.

## Criterios de Aceitacao

1. Poligono renderizado com cor por status
2. Esquema de cores intuitivo por workflow state
3. Popup com dados resumidos ao clicar
4. Acoes rapidas de editar e aprovar no popup
5. Clustering ou tiling para performance

## Rastreabilidade

- Modulos: REURBWEB, REURBCAD
- Requisitos dependentes: RF-049, RF-056
