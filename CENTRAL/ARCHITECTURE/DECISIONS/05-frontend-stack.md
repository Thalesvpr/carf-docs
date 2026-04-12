---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-005: React com TypeScript para Frontend

## Contexto

Portal web deve exibir mapas interativos, formularios complexos e dashboards com metricas. Componentizacao facilita reuso entre REURBWEB e REURBMASTER. TypeScript desejado para consistencia com bibliotecas compartilhadas. Decisao impacta produtividade e manutencao de longo prazo.

## Decisao

Adotamos React 18 com TypeScript e Vite como bundler. TanStack Query gerencia cache e estado servidor. Zustand para estado global simples. shadcn/ui fornece componentes acessiveis e customizaveis. react-leaflet integra mapas Leaflet com modelo React.

## Consequencias

Ecossistema vasto de bibliotecas e componentes. Reuso de conhecimento com React Native no mobile. Hot reload do Vite acelera desenvolvimento. Bundle size requer atencao com code splitting. Curva de aprendizado para hooks e estado reativo.

## Alternativas Rejeitadas

Vue.js foi descartado por ecossistema menor para GIS e incompatibilidade com React Native. Angular foi rejeitado por complexidade excessiva para escopo do projeto. Svelte foi descartado por imaturidade de bibliotecas de mapas e menor mercado de desenvolvedores.
