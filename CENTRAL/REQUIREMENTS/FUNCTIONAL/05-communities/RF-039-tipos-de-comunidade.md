---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-039: Tipos de Comunidade

## Descricao

Sistema deve suportar tipos predefinidos de comunidade: Assentamento Informal para ocupacoes irregulares sem infraestrutura completa, Reassentamento para areas destinadas a realocacao de familias, Area Urbanizada para regioes consolidadas com infraestrutura, Area Rural para comunidades em zona rural ou periurbana. Enum implementado em backend como tipo de dado restrito garantindo integridade referencial e consistencia de valores.

## Criterios de Aceitacao

1. Enum com tipos predefinidos no backend
2. Validacao de tipo obrigatoria antes de persistir
3. Erro HTTP 400 para tipos invalidos
4. Filtros por tipo disponiveis em listagens
5. Constantes exportadas para frontend

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-034
