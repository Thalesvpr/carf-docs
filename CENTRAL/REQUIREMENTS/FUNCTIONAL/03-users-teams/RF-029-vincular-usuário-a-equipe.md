---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-029: Vincular Usuario a Equipe

## Descricao

Usuarios com role ADMIN podem adicionar usuarios existentes a equipes. Selecao de usuarios ocorre atraves de interface de busca e selecao multipla filtrando por nome, email ou role. Usuario pode estar vinculado a multiplas equipes simultaneamente permitindo participacao em projetos cross-funcionais. Atualizacao de permissoes ocorre automaticamente apos vinculacao onde usuario passa a visualizar comunidades atribuidas a nova equipe sem necessidade de logout.

## Criterios de Aceitacao

1. Busca e selecao multipla de usuarios
2. Usuario pode pertencer a multiplas equipes
3. Atualizacao automatica de permissoes
4. Comunidades da equipe visiveis imediatamente
5. Gestao via edicao de equipe ou edicao de usuario

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-026, RF-021
