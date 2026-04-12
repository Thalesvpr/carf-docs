---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-073: Volume de Dados - Unidades

## Descricao

Sistema deve operar eficientemente com ate 1 milhao de unidades imobiliarias. Indices otimizados (B-tree, GiST para PostGIS). Table partitioning por tenant_id ou regiao quando necessario.

## Metricas

- Volume: ate 1 milhao de registros
- Queries criticas: <= 500ms
- Indices: B-tree para PKs/FKs, GiST para geometrias

## Criterios de Aceitacao

1. EXPLAIN ANALYZE revisado regularmente para queries criticas
2. Testes de performance com dados sinteticos em volume realista
3. Particionamento considerado para tabelas que excedam thresholds
