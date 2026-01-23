---
id: RNF-043
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-043: Monitoramento de Erros

## Descricao

Todos os modulos devem capturar e reportar erros automaticamente via Sentry ou similar. Permite identificacao rapida de problemas e priorizacao por frequencia e impacto.

## Metricas

- Ferramenta: Sentry, Rollbar ou similar
- Ambientes: producao e staging
- Contexto: user_id hash, tenant_id, versao, breadcrumbs (sem PII)

## Criterios de Aceitacao

1. Stack traces completos com source maps para codigo transpilado
2. Nenhuma PII enviada (sem CPF, email, senhas, tokens)
3. Alertas configurados para erros de alta severidade
