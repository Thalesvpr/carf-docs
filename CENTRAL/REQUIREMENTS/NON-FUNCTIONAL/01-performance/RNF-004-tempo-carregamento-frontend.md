---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-004: Tempo de Carregamento - Frontend

## Descricao

O modulo GEOWEB deve carregar a pagina inicial rapidamente para proporcionar feedback visual imediato ao usuario. Metricas Web Vitals garantem experiencia de carregamento adequada.

## Metricas

- First Contentful Paint (FCP): <= 3 segundos
- Largest Contentful Paint (LCP): <= 4 segundos
- Lighthouse performance score: >= 80
- Ferramenta de medicao: Google Lighthouse

## Criterios de Aceitacao

1. FCP e LCP dentro dos limites estabelecidos
2. Code splitting implementado para chunks sob demanda
3. Lazy loading de componentes React nao-criticos
