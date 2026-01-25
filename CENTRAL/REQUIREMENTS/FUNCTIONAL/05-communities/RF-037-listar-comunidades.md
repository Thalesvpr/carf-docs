---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-037: Listar Comunidades

## Descricao

Usuarios podem listar comunidades do tenant respeitando filtros de equipe conforme RF-030. Paginacao implementada retornando subconjunto configuravel de registros com controles de navegacao e metadados de total. Filtros disponiveis incluem tipo de comunidade, municipio, estado e status ativo/inativo. Busca textual por nome com matching parcial case-insensitive. Ordenacao personalizavel por data de criacao, nome, populacao ou area.

## Criterios de Aceitacao

1. Listagem paginada com metadados de navegacao
2. Filtro por tipo, municipio, estado e status
3. Busca por nome com correspondencia parcial
4. Ordenacao configuravel por multiplos campos
5. Filtro automatico por equipe conforme RF-030

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-030, RF-034
