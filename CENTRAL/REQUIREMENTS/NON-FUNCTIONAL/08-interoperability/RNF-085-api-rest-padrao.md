---
id: RNF-085
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-085: API REST Padrao

## Descricao

Endpoints seguem convencoes REST com verbos HTTP corretos: GET leitura, POST criacao (201), PUT substituicao, PATCH parcial, DELETE remocao (204). Versionamento via /v1 em URLs.

## Metricas

- Verbos: GET, POST, PUT, PATCH, DELETE semanticos
- Status: 200, 201, 204, 400, 401, 403, 404, 409, 500
- URLs: /api/v1/resources, /api/v1/resources/{id}

## Criterios de Aceitacao

1. Substantivos no plural para colecoes (/units, /communities)
2. Recursos aninhados quando apropriado (/communities/{id}/units)
3. Versionamento permite evolucao sem quebrar integradores
