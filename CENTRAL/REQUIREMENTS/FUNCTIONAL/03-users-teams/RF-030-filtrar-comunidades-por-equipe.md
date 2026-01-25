---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-030: Filtrar Comunidades por Equipe

## Descricao

Usuarios regulares (MANAGER, ANALYST, FIELD_AGENT) visualizam apenas comunidades atribuidas a sua equipe. Filtro automatico por equipe aplicado transparentemente em todas queries de listagem de comunidades. Usuarios com role ADMIN visualizam todas comunidades do tenant independente de vinculacao a equipes permitindo gestao global e reatribuicao entre equipes. Visualizacao restrita implementa Row Level Security baseado em equipe garantindo segregacao de dados e responsabilidades.

## Criterios de Aceitacao

1. Usuarios regulares veem apenas comunidades da equipe
2. Filtro aplicado automaticamente em todas queries
3. ADMIN visualiza todas comunidades do tenant
4. RLS baseado em equipe para segregacao
5. Filtro aplicado em camada de servico ou ORM

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-026, RF-013
