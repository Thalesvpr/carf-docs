---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-041: Estatisticas de Comunidade

## Descricao

Sistema deve calcular automaticamente estatisticas agregadas de comunidade incluindo contagem de unidades por status (DRAFT, PENDING, APPROVED, REJECTED) exibindo distribuicao percentual e quantidades absolutas. Total de titulares unicos vinculados a unidades calculado atraves de query agregada distinct. Area total em metros quadrados calculada utilizando funcoes geoespaciais do PostgreSQL (ST_Area) com conversao para hectares ou km2 conforme magnitude.

## Criterios de Aceitacao

1. Contagem de unidades por status com percentuais
2. Total de titulares unicos via query distinct
3. Area total calculada com ST_Area
4. Caching de estatisticas para performance
5. Exibicao em cards ou dashboard

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-044
