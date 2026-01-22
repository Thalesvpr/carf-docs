---
title: "Testing"
status: review
updated: 2026-01-21
---

# Testing

Testes com Testing Library e Vitest. Queries por role/label/text (nao por testId/className). userEvent para interacoes (click, type, keyboard). Assertions via expect().toHaveTextContent(), .toBeDisabled(), .toBeInTheDocument(). Acessibilidade com jest-axe via toHaveNoViolations(). Coverage minimo 80%. Comandos: `bun test`, `bun test --watch`, `bun test --coverage`. Mock data com tipos de @carf/tscore. Evitar testes de implementacao (estado interno, classes CSS).
