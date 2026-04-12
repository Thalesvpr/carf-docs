---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-062: Multiplos Titulares por Unidade

## Descricao

Sistema deve permitir que uma unidade habitacional tenha multiplos titulares vinculados simultaneamente com diferentes tipos de relacionamento e percentuais de propriedade. Implementacao utiliza tabela associativa unit_holders com campos relationship, ownership_percentage e is_primary. Sistema valida que soma dos percentuais nao ultrapasse 100% quando aplicavel. Apenas um titular pode ser marcado como principal por unidade garantindo identificacao clara do responsavel primario para comunicacoes e notificacoes.

## Criterios de Aceitacao

1. Suporte a multiplos titulares por unidade
2. Percentual de propriedade por titular
3. Validacao de soma de percentuais <= 100%
4. Apenas um titular principal por unidade
5. Tipos de relacionamento distintos por vinculo

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-061
