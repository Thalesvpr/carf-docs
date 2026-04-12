---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-020: Listar Tenants

## Descricao

Usuarios com role SUPER_ADMIN podem listar todos tenants cadastrados no sistema. Paginacao de resultados implementada retornando subconjunto configuravel com metadados de total de registros, pagina atual e total de paginas. Filtros disponiveis incluem status ativo/inativo e busca por nome com correspondencia parcial case-insensitive. Ordenacao personalizavel por data de criacao, nome alfabetico ou ultima atualizacao com direcao configuravel ascendente ou descendente.

## Criterios de Aceitacao

1. Listagem paginada com metadados de navegacao
2. Filtro por status ativo/inativo
3. Busca por nome com correspondencia parcial
4. Ordenacao configuravel por multiplos campos
5. Tabela com colunas nome, dominio, status e data criacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-017, RF-007
