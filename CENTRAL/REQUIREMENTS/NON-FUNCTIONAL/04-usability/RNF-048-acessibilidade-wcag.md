---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-048: Acessibilidade (WCAG 2.1)

## Descricao

GEOWEB deve implementar nivel AA de acessibilidade conforme WCAG 2.1. Garante uso por pessoas com deficiencias visuais, motoras e cognitivas.

## Metricas

- Contraste: minimo 4.5:1 para textos normais
- Lighthouse: score de acessibilidade >= 90
- Screen readers: compativel com NVDA e VoiceOver

## Criterios de Aceitacao

1. Navegacao completa via teclado sem focus traps
2. Labels explicitas em todos inputs de formulario
3. Semantica HTML adequada com ARIA onde necessario
