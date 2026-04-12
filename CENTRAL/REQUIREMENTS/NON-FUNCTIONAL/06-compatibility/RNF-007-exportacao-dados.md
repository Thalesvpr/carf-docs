---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-007: Exportacao de Dados

## Descricao

Exportacoes pequenas (ate 1000 registros) geradas em 10 segundos. Exportacoes grandes processadas em background com notificacao e link de download expirando em 24h.

## Metricas

- Pequenas: <= 10s para ate 1000 registros
- Grandes: background job com notificacao
- Formatos: CSV, XLSX, GeoJSON, Shapefile, PDF

## Criterios de Aceitacao

1. Exportacoes > 1000 registros processadas assincronamente
2. Link de download com expiracao de 24 horas
3. Streaming para exportacoes grandes sem carregar tudo em memoria
