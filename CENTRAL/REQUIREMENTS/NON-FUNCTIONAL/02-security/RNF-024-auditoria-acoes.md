---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-024: Auditoria de Acoes

## Descricao

GEOAPI deve manter registro completo e imutavel de acoes criticas para rastreabilidade, investigacao de incidentes e compliance LGPD. Logs estruturados em tabela append-only.

## Metricas

- Retencao: minimo 5 anos
- Armazenamento: tabela append-only no PostgreSQL
- Gravacao: assincrona para nao impactar latencia

## Criterios de Aceitacao

1. Login/logout registrados com timestamp, IP e user agent
2. CRUD de dados de dominio gera entrada de auditoria
3. Mudancas de permissoes auditadas com valores antes/depois
