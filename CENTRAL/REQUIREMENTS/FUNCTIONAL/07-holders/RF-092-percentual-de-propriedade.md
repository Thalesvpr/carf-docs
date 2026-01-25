---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-092: Percentual de Propriedade

## Descricao

Sistema deve permitir especificacao de percentual de propriedade para vinculo titular-unidade atraves de campo ownership_percentage com valores 0-100. Validacao garante que soma de percentuais de todos titulares da unidade totalize 100% quando aplicavel a proprietarios e possuidores. Para tipos onde percentual nao se aplica (LOCATARIO, USUFRUTUARIO) campo pode ser vazio. Interface exibe percentuais formatados com simbolo % e ate duas casas decimais, alem de grafico visual de distribuicao.

## Criterios de Aceitacao

1. Campo ownership_percentage (0-100)
2. Validacao de soma = 100% quando aplicavel
3. Campo opcional para tipos sem percentual
4. Formatacao com simbolo % e decimais
5. Grafico de distribuicao de propriedade

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-091, RF-062
