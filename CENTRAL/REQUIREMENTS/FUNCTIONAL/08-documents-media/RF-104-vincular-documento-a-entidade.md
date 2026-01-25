---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-104: Vincular Documento a Entidade

## Descricao

Sistema deve permitir vinculacao polimorfica de documentos a diferentes tipos de entidades atraves de campos entity_type (UNIT, HOLDER, COMMUNITY) e entity_id. Arquitetura polimorfica permite reutilizar mesmo modelo para documentos de unidades, titulares e comunidades. Validacao garante integridade referencial verificando que entity_id existe na tabela correspondente. Indices compostos em (entity_type, entity_id) garantem performance otimizada. Upload contextual vincula automaticamente a entidade visualizada.

## Criterios de Aceitacao

1. Campos entity_type e entity_id
2. Tipos: UNIT, HOLDER, COMMUNITY
3. Validacao de integridade referencial
4. Indices compostos para performance
5. Vinculacao automatica no upload contextual

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-102, RF-049, RF-084, RF-034
