---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
---

# RF-066: Desenhar Unidade no Mapa

## Descricao

Sistema deve permitir desenho de poligonos representando unidades habitacionais diretamente no mapa interativo. Ferramentas de desenho incluem criacao de poligonos por clique sequencial de vertices e retangulos por arrastar diagonal. Opcao de snap-to-grid alinha automaticamente vertices a grade configuravel. Edicao de vertices individualmente permitindo arrastar, adicionar e remover pontos. Validacao automatica de geometria verificando auto-interseccao.

## Criterios de Aceitacao

1. Desenho de poligono por clique de vertices
2. Ferramenta de retangulo por arrastar
3. Snap-to-grid configuravel
4. Edicao de vertices individual
5. Validacao de geometria em tempo real

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD
- Requisitos dependentes: RF-049, RF-068
