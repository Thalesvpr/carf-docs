---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-068: Calcular Area da Unidade

## Descricao

Sistema deve calcular automaticamente a area de cada unidade habitacional a partir de sua geometria espacial. Calculo realizado no backend utilizando funcoes nativas do PostGIS (ST_Area) com projecao adequada que preserve medidas de superficie. Area calculada em metros quadrados com configuracao de SRID apropriado para regiao geografica. Campo de area atualizado automaticamente via triggers quando geometria for criada ou modificada. Frontend exibe area formatada com separador de milhares e duas casas decimais.

## Criterios de Aceitacao

1. Calculo automatico via PostGIS ST_Area
2. Projecao adequada para precisao de medidas
3. Atualizacao automatica ao modificar geometria
4. Formatacao com separador de milhares
5. Exibicao em metros quadrados (m²)

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049, RF-066
