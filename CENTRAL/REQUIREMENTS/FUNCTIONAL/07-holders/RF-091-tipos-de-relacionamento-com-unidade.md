---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-091: Tipos de Relacionamento com Unidade

## Descricao

Sistema deve suportar categorizacao de vinculos entre titulares e unidades atraves de tipos predefinidos: PROPRIETARIO, POSSUIDOR, USUFRUTUARIO, LOCATARIO, COMODATARIO, OUTRO. Cada tipo representa natureza juridica especifica da relacao pessoa-imovel. Implementacao via enumeracao no campo relationship da tabela unit_holders. Cada tipo pode ter validacoes especificas como percentual de propriedade aplicavel apenas a proprietarios. Interface apresenta seletor com descricoes claras de cada categoria durante vinculacao.

## Criterios de Aceitacao

1. Enum com tipos de relacionamento predefinidos
2. Campo relationship na tabela unit_holders
3. Opcao OUTRO com texto livre
4. Validacoes especificas por tipo
5. Descricoes claras no seletor

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-061, RF-092
