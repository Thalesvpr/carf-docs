---
title: "Build and Run"
status: review
updated: 2026-01-21
---

# Build and Run

Build com `bun run build` gerando dist/ (ESM, CJS, .d.ts, sourcemaps). Testes com `bun test` (coverage >80%). Type check com `tsc --noEmit`. Lint com `bun run lint`. Publicacao: configurar .npmrc com GITHUB_TOKEN, rodar build e test, `npm version patch`, `git push --tags`, `npm publish`. Versionamento semantico: PATCH para bug fixes, MINOR para novas features, MAJOR para breaking changes.
