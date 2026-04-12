---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-105: Listar Documentos

## Descricao

Sistema deve oferecer listagem de documentos com filtro por entidade permitindo visualizar arquivos anexados a unidade, titular ou comunidade especifica. Paginacao automatica garante performance. Listagem apresenta nome, tipo, tamanho formatado e data de upload. Preview visual com thumbnails para imagens e icones tipificados para PDFs. Acoes contextuais incluem visualizar, baixar, editar metadados e excluir com confirmacao. Busca textual filtra por nome ou tipo.

## Criterios de Aceitacao

1. Filtro por entidade (entity_type + entity_id)
2. Paginacao automatica
3. Preview visual (thumbnails e icones)
4. Acoes: visualizar, baixar, editar, excluir
5. Busca textual por nome ou tipo

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-102, RF-104
