---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-055: Tipos de Unidade

## Descricao

Sistema deve suportar categorizacao de unidades habitacionais atraves de tipos predefinidos: RESIDENCIAL, COMERCIAL, MISTO, INSTITUCIONAL, EQUIPAMENTO_PUBLICO. Cada tipo representa o uso predominante da edificacao e influencia regras de validacao e apresentacao de dados. Implementacao utiliza enumeracao (enum) no backend garantindo valores consistentes. Filtros por tipo disponiveis em listagens e consultas para analises demograficas e planejamento urbano.

## Criterios de Aceitacao

1. Enum com tipos predefinidos no backend
2. Validacao de tipo obrigatoria antes de persistir
3. Erro HTTP 400 para tipos invalidos
4. Filtros por tipo disponiveis em listagens
5. Constantes exportadas para frontend

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049
