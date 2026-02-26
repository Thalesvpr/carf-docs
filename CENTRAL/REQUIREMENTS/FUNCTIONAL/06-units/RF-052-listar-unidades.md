---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-052: Listar Unidades

## Descricao

Usuarios podem listar unidades com paginacao e filtros avancados. Paginacao implementada retornando subconjunto configuravel de registros com metadados de navegacao. Filtros disponiveis incluem status de workflow (DRAFT, PENDING, APPROVED, REJECTED), comunidade vinculada, tipo de unidade e periodo de criacao. Busca textual por endereco, codigo ou nome de titular com matching case-insensitive. Ordenacao personalizavel por data, codigo, endereco ou area.

## Criterios de Aceitacao

1. Listagem paginada com metadados de navegacao
2. Filtros por status, comunidade, tipo e periodo
3. Busca por endereco, codigo ou titular
4. Ordenacao configuravel por multiplos campos
5. Exportacao de resultados filtrados

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-056
