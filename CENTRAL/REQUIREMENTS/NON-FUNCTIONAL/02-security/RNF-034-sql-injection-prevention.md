---
id: RNF-034
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-034: SQL Injection Prevention

## Descricao

GEOAPI deve usar exclusivamente Entity Framework Core com queries parametrizadas. Elimina concatenacao de strings de usuario em SQL, causa primaria de SQL injection.

## Metricas

- ORM: Entity Framework Core obrigatorio
- Queries: LINQ ou FromSqlRaw com parametros
- SAST: analise estatica no CI/CD para detectar SQL inseguro

## Criterios de Aceitacao

1. Nenhuma concatenacao de strings em contextos de SQL
2. FromSqlRaw/ExecuteSqlRaw sempre com placeholders parametrizados
3. Credencial do banco com privilegio minimo (sem DROP/CREATE/ALTER)
