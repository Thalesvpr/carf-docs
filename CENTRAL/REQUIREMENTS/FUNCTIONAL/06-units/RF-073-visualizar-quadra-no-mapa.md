---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-073: Visualizar Quadra no Mapa

## Descricao

Sistema deve renderizar quadras no mapa interativo REURBWEB mostrando contorno geometrico quando definido. Estilo visual diferencia quadras de unidades atraves de espessura de linha, cor e transparencia. Dentro do contorno, unidades vinculadas exibidas com coloracao baseada em status (DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, CHANGES_REQUESTED). Popup ao clicar ou hover apresenta estatisticas agregadas: nome, codigo, total de unidades e distribuicao por status. Visualizacao facilita identificacao de quadras problematicas.

## Criterios de Aceitacao

1. Renderizacao de contorno da quadra
2. Estilo visual diferenciado de unidades
3. Coloracao de unidades por status
4. Popup com estatisticas agregadas
5. Distribuicao de unidades por status

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-070, RF-053
