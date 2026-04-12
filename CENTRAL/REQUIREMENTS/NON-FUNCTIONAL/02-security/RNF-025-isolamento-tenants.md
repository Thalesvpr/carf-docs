---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-025: Isolamento de Tenants

## Descricao

Dados entre tenants (municipios) devem ser rigorosamente isolados via Row Level Security no PostgreSQL e validacoes no GEOAPI. Impossibilita acesso cross-tenant mesmo com bugs ou bypass deliberado.

## Metricas

- Mecanismo: Row Level Security (RLS) no PostgreSQL
- Coluna: tenant_id em todas tabelas de dominio
- Defesa em profundidade: filtro no banco + middleware na aplicacao

## Criterios de Aceitacao

1. RLS habilitado em todas tabelas com dados de tenant
2. Contexto de tenant extraido do JWT e configurado na sessao PostgreSQL
3. Testes automatizados validam impossibilidade de acesso cross-tenant
