---
id: RNF-049
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-049: Feedback Visual

## Descricao

Sistema deve fornecer feedback visual claro para todas operacoes assincronas. Usuario deve sempre saber estado atual, se acao foi registrada ou se ocorreu erro.

## Metricas

- Loading: spinner apos 300ms de espera
- Toasts: 3-5 segundos para sucesso, persistente para erros
- Transicoes: duracao de 200-300ms

## Criterios de Aceitacao

1. Loading spinners ou skeleton screens em operacoes > 300ms
2. Progress bars com percentual para uploads e exportacoes
3. Botoes desabilitados durante processamento (anti-duplo-click)
