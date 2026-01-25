---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-051: Undo/Redo

## Descricao

GEOWEB deve implementar confirmacao e reversao para acoes destrutivas. Reduz ansiedade do usuario e permite recuperacao rapida de erros acidentais.

## Metricas

- Toast undo: timeout de 5-10 segundos para reverter
- Historico: minimo 20 niveis em editores complexos
- Atalhos: Ctrl+Z (desfazer), Ctrl+Shift+Z (refazer)

## Criterios de Aceitacao

1. Modal de confirmacao para exclusoes permanentes de registros
2. Toast com botao Desfazer para acoes reversiveis
3. Undo/redo via teclado em editores de geometria
