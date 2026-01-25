---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-044: Logs Estruturados

## Descricao

Logs em formato JSON com campos padronizados: timestamp ISO 8601, level, message, request_id, user_id, tenant_id. Agregacao via ELK/Loki. Correlacao por request_id atraves de toda a stack.

## Metricas

- Formato: JSON com campos padronizados
- Niveis: ERROR, WARN, INFO, DEBUG
- Retencao: minimo 30 dias
- Busca: < 5s para queries do ultimo dia

## Criterios de Aceitacao

1. Request_id unico gerado e propagado em todos os logs da requisicao
2. Logs agregados em sistema centralizado (ELK, Loki)
3. Busca eficiente por user_id, tenant_id, error_type
