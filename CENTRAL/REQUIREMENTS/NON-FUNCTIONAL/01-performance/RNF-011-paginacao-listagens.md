---
id: RNF-011
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-011: Paginacao de Listagens

## Descricao

Listagens do GEOAPI devem suportar paginacao eficiente para grandes volumes de dados. Usuarios devem navegar rapidamente independente da pagina acessada.

## Metricas

- Capacidade: ate 100.000 registros paginaveis
- Tempo de resposta: <= 500ms para qualquer pagina
- Limite de pageSize: maximo 100 registros por pagina

## Criterios de Aceitacao

1. Cursor-based pagination implementado para grandes volumes
2. Indices criados nas colunas utilizadas para ordenacao
3. Qualquer pagina do conjunto responde em ate 500ms
