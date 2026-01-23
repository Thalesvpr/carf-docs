---
id: RNF-012
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-012: Cache de Dados

## Descricao

Dados frequentemente acessados cacheados em Redis. Reduz carga no banco de dados e melhora tempos de resposta para consultas repetidas. TTL configuravel por tipo de dado.

## Metricas

- Hit rate: >= 70%
- TTL listagens: 5 minutos
- TTL estatisticas/dashboards: 15 minutos

## Criterios de Aceitacao

1. Cache-aside pattern com verificacao antes de consulta ao banco
2. Invalidacao automatica quando dados subjacentes sao modificados
3. Cache keys estruturadas por tenant, entidade e parametros
