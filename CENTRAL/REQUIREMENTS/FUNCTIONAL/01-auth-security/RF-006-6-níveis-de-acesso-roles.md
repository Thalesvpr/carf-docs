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

# RF-006: 6 Niveis de Acesso (Roles)

## Descricao

O sistema deve suportar seis niveis hierarquicos de acesso baseados em roles: SUPER_ADMIN com privilegios globais irrestritos, ADMIN com gestao de tenant especifico, MANAGER com aprovacao de workflows, ANALYST com cadastro e edicao de dados, FIELD_COORDINATOR com supervisao de equipe de campo e menu mobile completo, FIELD_CADASTRATOR com coleta de dados em campo restrito a mapa e formularios. Roles definidos no Keycloak e mapeados para permissoes no backend via claims JWT.

## Criterios de Aceitacao

1. Seis roles distintos configurados no Keycloak
2. Cada role possui conjunto especifico de permissoes
3. Hierarquia respeitada (SUPER_ADMIN herda todas permissoes)
4. Role presente no claim roles do JWT
5. Interface exibe apenas funcionalidades permitidas para role do usuario

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB, REURBCAD, GEOGIS
- Requisitos dependentes: RF-001, RF-005
