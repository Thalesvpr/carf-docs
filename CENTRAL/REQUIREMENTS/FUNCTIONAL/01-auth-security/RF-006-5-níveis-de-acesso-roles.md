---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - GEOWEB
  - REURBCAD
  - GEOGIS
---

# RF-006: 5 Niveis de Acesso (Roles)

## Descricao

O sistema deve suportar cinco niveis hierarquicos de acesso baseados em roles: SUPER_ADMIN com privilegios globais irrestritos, ADMIN com gestao de tenant especifico, MANAGER com aprovacao de workflows, ANALYST com cadastro e edicao de dados, FIELD_AGENT com coleta de dados em campo. Roles definidos no Keycloak e mapeados para permissoes no backend via claims JWT.

## Criterios de Aceitacao

1. Cinco roles distintos configurados no Keycloak
2. Cada role possui conjunto especifico de permissoes
3. Hierarquia respeitada (SUPER_ADMIN herda todas permissoes)
4. Role presente no claim roles do JWT
5. Interface exibe apenas funcionalidades permitidas para role do usuario

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB, REURBCAD, GEOGIS
- Requisitos dependentes: RF-001, RF-005
