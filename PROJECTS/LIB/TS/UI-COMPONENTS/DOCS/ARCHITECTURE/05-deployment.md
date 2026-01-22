---
title: "Deployment"
status: review
updated: 2026-01-21
---

# Deployment

Publicada como NPM package via GitHub Packages. Build com Vite/tsup gerando ESM e CommonJS, .d.ts types e source maps. Tree-shaking enabled, peer dependencies externalizadas (React, Tailwind). Package.json com exports field para subpaths (@carf/ui/button). Workflow automatizado: tag v*.*.* aciona GitHub Actions que executa build, test e npm publish. Versioning semantico: MAJOR para breaking changes em props, MINOR para novas features, PATCH para bug fixes.
