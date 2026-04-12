---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-063: Tratamento de Excecoes

## Descricao

Exception filters globais capturam erros e mapeiam para HTTP correto: 400 validacao, 401 autenticacao, 403 autorizacao, 404 nao encontrado, 409 conflito, 500 interno. Logs com stack trace e correlation ID.

## Metricas

- Mapeamento: erros para status HTTP semantico
- Logs: stack trace, contexto, correlation ID
- Formato: codigo de erro, mensagem em portugues, timestamp

## Criterios de Aceitacao

1. Nenhum stack trace exposto ao usuario final
2. Todas excecoes registradas com contexto para debugging
3. Correlation ID permite localizar logs do erro
