---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-147: Snap to Features

## Descricao

Sistema deve oferecer funcionalidade de snap durante edicao ou criacao de features, permitindo que vertices desenhados colem automaticamente em features existentes quando cursor se aproxima, facilitando criacao de topologia precisa e conectividade entre elementos geograficos. Tolerancia de snap configuravel especifica distancia em pixels (tipicamente 10 a 20 pixels) dentro da qual snap e ativado, permitindo ajuste conforme densidade de features e preferencias do usuario. Interface fornece indicacao visual clara de snap ativado com feedback imediato (mudanca de cor do cursor, highlight do vertice alvo ou linha guia). Sistema permite ativacao e desativacao via toggle ou tecla modificadora (Ctrl) para controle quando desenho proximo mas nao conectado e necessario. Snap funciona com vertices, edges e centroides de features existentes.

## Criterios de Aceitacao

1. Tolerancia de snap configuravel em pixels
2. Indicacao visual de snap ativado
3. Toggle para ativar/desativar
4. Snap em vertices, edges e centroides
5. Tecla modificadora para bypass

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-132, RF-133
