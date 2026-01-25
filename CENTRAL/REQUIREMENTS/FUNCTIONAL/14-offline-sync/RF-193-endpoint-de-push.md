---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-193: Endpoint de Push

## Descricao

GEOAPI deve disponibilizar endpoint POST /api/sync/push que recebe dados criados ou editados offline pelos aplicativos moveis, aceitando payload com array de changes onde cada elemento representa operacao de criacao, atualizacao ou delecao a ser aplicada no banco central. Endpoint implementa validacao rigorosa verificando conformidade com schema, campos obrigatorios, tipos de dados e constraints de negocio como unicidade e integridade referencial, rejeitando operacoes invalidas com mensagens de erro descritivas. Durante processamento, sistema executa deteccao de conflitos comparando timestamps de ultima atualizacao. Resposta retorna mapeamento de IDs onde UUIDs gerados localmente sao associados aos IDs definitivos do servidor, permitindo que cliente atualize referencias locais e estabeleca correspondencia entre registros temporarios e permanentes.

## Criterios de Aceitacao

1. Endpoint POST /api/sync/push
2. Validacao rigorosa de schema e constraints
3. Deteccao de conflitos por timestamp
4. Mapeamento de UUIDs locais para IDs do servidor
5. Mensagens de erro descritivas

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-017, RF-190
