---
id: RNF-089
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-089: Timezone

## Descricao

Timestamps armazenados em UTC no banco de dados, convertidos para timezone local no frontend. Formato ISO 8601 para serializacao em APIs. Elimina ambiguidades de horario de verao e fusos regionais.

## Metricas

- Armazenamento: timestamp with time zone do PostgreSQL em UTC
- Serializacao: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)
- Biblioteca: date-fns-tz ou similar com database IANA

## Criterios de Aceitacao

1. Timestamps no banco sempre em UTC verificavel via query
2. APIs retornam formato ISO 8601 com indicador Z ou offset
3. Frontend converte e exibe em timezone local do usuario
