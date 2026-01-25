---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-051: Excluir Unidade

## Descricao

Usuarios com role ADMIN podem excluir unidade utilizando soft delete onde registro e marcado como deletado atraves de flag deleted_at timestamp sem remocao fisica de dados. Preservacao de dados para auditoria mantem registro completo incluindo geometria, atributos, titulares vinculados e documentos anexados. Unidades deletadas removidas de visualizacao padrao atraves de filtros automaticos WHERE deleted_at IS NULL, mas acessiveis em contextos administrativos.

## Criterios de Aceitacao

1. Soft delete com flag deleted_at timestamp
2. Preservacao completa de dados para auditoria
3. Remocao de listagens e mapas padrao
4. Visivel para ADMIN com filtro de deletados
5. Opcao de restauracao (undelete) disponivel

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-008
