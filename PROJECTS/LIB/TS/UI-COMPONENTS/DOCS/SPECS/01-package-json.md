---
type: leaf
title: "Package.json"
status: review
updated: 2026-01-21
---

# Package.json

Configuracao @carf/ui. Type module, main dist/index.js, types dist/index.d.ts, sideEffects apenas CSS. Exports: "." para bundle principal, "./globals.css" e "./tailwind.config". Dependencies: class-variance-authority, clsx, tailwind-merge. Peer dependencies: React 18, Radix UI primitives, lucide-react, tailwindcss. Dev: Storybook 7, Testing Library, Vite, Vitest, TypeScript 5.3. Scripts: build (vite + tsc), dev, storybook, test, lint, type-check. Publicacao via GitHub Packages com SemVer.
