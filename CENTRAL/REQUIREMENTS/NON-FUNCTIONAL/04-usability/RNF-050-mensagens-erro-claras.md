---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-050: Mensagens de Erro Claras

## Descricao

Mensagens de erro devem ser compreensiveis e acionaveis em linguagem natural. Proibido exibir stack traces, codigos HTTP ou jargao tecnico ao usuario final.

## Metricas

- Linguagem: natural, sem termos tecnicos
- Contexto: identifica campo ou operacao problematica
- Acao: inclui sugestao de correcao

## Criterios de Aceitacao

1. Nenhum stack trace ou codigo HTTP exibido ao usuario
2. Erros de validacao destacam campos com borda colorida
3. Cada mensagem inclui sugestao de acao corretiva
