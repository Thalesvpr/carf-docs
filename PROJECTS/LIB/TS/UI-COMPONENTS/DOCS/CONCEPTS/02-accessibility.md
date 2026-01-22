---
type: leaf
title: "Accessibility"
status: review
updated: 2026-01-21
---

# Accessibility

WCAG 2.1 AA obrigatorio em todos componentes. Navegacao por teclado: Tab para foco, Enter/Space para ativar, Escape para fechar, Arrows para navegar opcoes. ARIA: roles corretos (button, dialog, menu), aria-expanded, aria-selected, aria-invalid com aria-describedby para erros. Contraste minimo 4.5:1 para texto, 3:1 para UI. Focus trap em modais com retorno de foco ao fechar. Live regions (aria-live="polite") para Toast e Alert. Reduced motion respeitado via media query. Testes automatizados com axe-core no CI e manual com NVDA/VoiceOver em releases.
