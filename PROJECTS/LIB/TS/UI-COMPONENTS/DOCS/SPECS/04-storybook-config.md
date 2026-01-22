---
title: "Storybook Config"
status: review
updated: 2026-01-21
---

# Storybook Config

Configuracao Storybook 7 com Vite. Estrutura: .storybook/ com main.ts, preview.ts, manager.ts, theme.ts. Addons: links, essentials, interactions, a11y. Stories em src/**/*.stories.tsx. Preview com globals.css, backgrounds (light, dark, carf-primary), viewports (mobile, tablet, desktop), decorator para dark mode. Manager com tema CARF customizado (cores verde, branding). Stories seguem template Meta/StoryObj com argTypes para controles. Domain components usam mock data tipado. Comandos: `bun run storybook` (dev), `bun run build-storybook` (static).
