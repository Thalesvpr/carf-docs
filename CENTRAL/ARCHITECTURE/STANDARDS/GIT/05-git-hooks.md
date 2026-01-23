---
type: leaf
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING. Stub de 9 linhas - incompleto."
updated: 2026-01-19
---

# Git Hooks

Git hooks automatizando checks do CARF via Husky. pre-commit (lint staged files ESLint/Prettier frontend, dotnet format backend, validar no console.log committed, run quick tests affected files). commit-msg (commitlint validando Conventional Commits format, reject se inválido). pre-push (run full test suite, lint all files, build success, prevent push se failing). Setup: npm install husky lint-staged, husky install creating .husky/ folder, configure .husky/pre-commit script. Benefits: catch issues early antes PR, enforce standards automaticamente, improve code quality. Bypass hooks (git commit --no-verify) apenas emergências documentadas.
