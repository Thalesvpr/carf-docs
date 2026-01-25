---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-024: Listar Usuarios

## Descricao

Usuarios com role ADMIN podem listar usuarios do proprio tenant. Paginacao implementada retornando subconjunto configuravel de registros com metadados de navegacao. Filtros disponiveis incluem role especifica, status ativo/inativo e equipe vinculada. Busca textual por nome ou email com matching parcial case-insensitive facilita localizacao rapida. Interface exibe tabela com colunas essenciais incluindo nome, email, role, status e data do ultimo acesso.

## Criterios de Aceitacao

1. Listagem paginada com metadados de navegacao
2. Filtro por role, status e equipe
3. Busca por nome ou email com correspondencia parcial
4. Exibicao de colunas essenciais na tabela
5. Acoes rapidas de editar, visualizar e desativar

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-021, RF-008
