---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-048: Atribuir Comunidade a Equipe

## Descricao

Usuarios com role ADMIN podem atribuir comunidades a equipes especificas. Multiplas equipes podem ser vinculadas a mesma comunidade permitindo colaboracao entre times. Controle de visibilidade automatico onde membros de equipes vinculadas visualizam comunidade e podem acessar unidades relacionadas. Filtros automaticos aplicados em queries conforme RF-030 garantindo que usuarios vejam apenas comunidades sob responsabilidade de suas equipes.

## Criterios de Aceitacao

1. Atribuicao de multiplas equipes a comunidade
2. Controle automatico de visibilidade
3. Membros de equipes vinculadas acessam unidades
4. Filtro automatico por equipe conforme RF-030
5. Log de alteracoes de atribuicao

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-026, RF-030
