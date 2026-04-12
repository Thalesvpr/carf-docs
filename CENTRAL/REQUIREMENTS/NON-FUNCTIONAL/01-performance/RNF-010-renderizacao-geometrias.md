---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-010: Renderizacao de Geometrias

## Descricao

O componente de mapa deve renderizar grandes volumes de geometrias sem lag perceptivel durante interacoes. Aplica-se aos modulos REURBWEB e REURBCAD que utilizam mapas como interface principal.

## Metricas

- Capacidade: 5000 poligonos renderizados em ate 2 segundos
- Taxa de quadros: >= 30 FPS durante interacoes (zoom, pan)
- Ferramenta de medicao: Chrome DevTools Performance

## Criterios de Aceitacao

1. 5000 geometrias visiveis sem degradacao de performance
2. Clustering implementado para agrupamento em zoom afastado
3. WebGL habilitado via MapLibre GL JS
