---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-026: Criar Equipe

## Descricao

Usuarios com role ADMIN podem criar equipes para organizar usuarios em grupos logicos. Formulario inclui nome descritivo da equipe, descricao de responsabilidades, vinculacao inicial de usuarios membros atraves de selecao multipla e atribuicao de comunidades especificas sob responsabilidade da equipe. Mesmo usuario pode pertencer a varias equipes facilitando colaboracao cross-funcional. Comunidades atribuidas definem escopo de trabalho da equipe onde membros visualizam prioritariamente essas comunidades.

## Criterios de Aceitacao

1. Formulario com nome, descricao e membros
2. Selecao multipla de usuarios para vinculacao
3. Atribuicao de comunidades a equipe
4. Usuario pode pertencer a multiplas equipes
5. Escopo de visualizacao definido por equipe

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-021, RF-008
