---
type: leaf
title: "Integration"
status: review
updated: 2026-01-21
---

# Integration

Consumida via NPM install do GitHub Packages com tree-shaking automatico. Aplicacoes devem configurar Tailwind content paths para incluir node_modules/@carf/ui. Theme via CSS variables (--primary, --radius) em globals.css. Integracao com Zustand para client state (filtros, preferencias), TanStack Query para server state (cache, refetch, optimistic updates), React Hook Form + Zod para formularios. Compativel com Next.js (App Router), Astro (islands), Keycloakify (temas de login). Domain components recebem types de @carf/tscore como props. Testes E2E com Playwright.
