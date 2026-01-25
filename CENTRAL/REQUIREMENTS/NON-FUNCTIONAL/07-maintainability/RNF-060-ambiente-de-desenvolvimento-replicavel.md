---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-060: Ambiente de Desenvolvimento Replicavel

## Descricao

Ambiente configuravel em menos de 15 minutos via Docker Compose. Inclui PostgreSQL/PostGIS, Redis, Keycloak, MinIO. Dados de seed para desenvolvimento imediato.

## Metricas

- Setup: < 15 minutos para ambiente funcional
- Docker Compose: todos os servicos em um comando
- Seed: dados representativos de todas as entidades

## Criterios de Aceitacao

1. Documentacao atualizada com pre-requisitos e troubleshooting
2. Mesmo ambiente em Windows, macOS e Linux
3. Desenvolvedores podem testar funcionalidades imediatamente
