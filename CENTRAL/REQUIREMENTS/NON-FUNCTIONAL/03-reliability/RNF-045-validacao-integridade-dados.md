---
id: RNF-045
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-045: Validacao de Integridade

## Descricao

GEOAPI deve implementar multiplas camadas de validacao de integridade de dados. Previne corrupcao, inconsistencias relacionais e erros de geometrias espaciais.

## Metricas

- Foreign keys: todas relacoes com constraints definidas
- Geometrias: validacao ST_IsValid() antes de insercao
- Checksums: SHA-256 para todos arquivos uploaded

## Criterios de Aceitacao

1. FK constraints em todas tabelas com politica DELETE documentada
2. Geometrias invalidas rejeitadas automaticamente via trigger
3. Verificacao periodica de checksums detecta corrupcao de arquivos
