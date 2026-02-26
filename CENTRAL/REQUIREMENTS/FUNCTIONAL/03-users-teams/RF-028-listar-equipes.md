---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-028: Listar Equipes

## Descricao

Usuarios com role ADMIN podem listar equipes do tenant. Paginacao implementada para navegacao eficiente em grandes quantidades de equipes retornando subconjunto de registros com controles de navegacao. Filtros disponiveis incluem busca por nome de equipe, quantidade de membros, comunidades atribuidas e status ativo/inativo. Exibicao de membros diretamente na listagem mostra avatares ou nomes de integrantes principais com indicacao de quantidade total.

## Criterios de Aceitacao

1. Listagem paginada com controles de navegacao
2. Filtro por nome, quantidade de membros e status
3. Exibicao de membros resumida na listagem
4. Acoes rapidas de editar e visualizar detalhes
5. Ordenacao configuravel por nome ou data criacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-026, RF-008
