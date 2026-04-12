---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-087: Listar Titulares

## Descricao

Sistema deve oferecer listagem paginada de titulares com busca e filtragem. Interface permite pesquisa textual por nome, CPF/CNPJ ou email com correspondencia parcial. Filtros incluem tipo de titular (PESSOA_FISICA, PESSOA_JURIDICA) e status (ativo, inativo). Paginacao automatica garante performance com grandes volumes. Ordenacao por diferentes campos via clique em cabecalhos. Metadados incluem total de registros e pagina atual.

## Criterios de Aceitacao

1. Busca textual por nome, documento ou email
2. Filtros por tipo e status
3. Paginacao automatica
4. Ordenacao por multiplos campos
5. Correspondencia parcial (substring)

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-084
