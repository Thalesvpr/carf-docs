---
type: standard
status: review
updated: 2026-01-22
---

# STD-016: Stack Frontend Web

## Regra

Frontend web deve usar React 18+ com TypeScript, Vite como bundler, shadcn/ui para componentes, TanStack Query para server state, Zustand para client state.

## Justificativa

Stack moderna com DX excelente. Vite tem build rapido. shadcn permite customizacao total. TanStack Query gerencia cache e sync. Zustand e minimalista.

## Aplicacao

Projetos GEOWEB, ADMIN e qualquer novo frontend web. Componentes compartilhados via workspace monorepo.
