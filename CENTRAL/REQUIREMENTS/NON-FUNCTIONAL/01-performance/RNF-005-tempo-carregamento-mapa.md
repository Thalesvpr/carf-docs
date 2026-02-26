---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-005: Tempo de Carregamento - Mapa

## Descricao

A renderizacao inicial do componente de mapa no REURBWEB deve ser rapida para permitir interacao imediata. Tempo medido ate o mapa estar completamente interativo (zoom, pan, cliques).

## Metricas

- Tempo ate interativo: <= 2 segundos
- Condicoes: primeira visita com cache limpo
- Ferramenta de medicao: Performance API do browser

## Criterios de Aceitacao

1. Mapa interativo em ate 2 segundos apos inicio do carregamento
2. Carregamento progressivo de tiles implementado
3. Cache de tiles habilitado para visitas subsequentes
