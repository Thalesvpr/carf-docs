---
type: leaf
status: review
updated: 2026-02-08
---

# CommunityType

Value object enum representando tipo de comunidade ou assentamento conforme classificacao da Lei 13.465/2017 de regularizacao fundiaria, determinando legislacao aplicavel, requisitos documentais e processos especificos. No banco de dados, corresponde ao campo communities.community_type (varchar(30)) com CHECK constraint.

O tipo de comunidade influencia diretamente quais regras de validacao sao aplicadas no cadastro de unidades e no processo de legitimacao fundiaria.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| URBANA | Nucleo urbano informal aplicando REURB-S (social) ou REURB-E (empresarial). |
| RURAL | Assentamento em zona rural seguindo regulamentacao INCRA. |
| QUILOMBOLA | Comunidade quilombola com titulacao coletiva conforme Decreto 4887/2003. |
| RIBEIRINHA | Comunidade tradicional as margens de rios com particularidades de ocupacao sazonal. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Legislacao aplicavel | Cada tipo aplica conjunto diferente de normas legais. |
| Titulacao coletiva | Apenas QUILOMBOLA permite titulacao coletiva. |
| Licenciamento ambiental | RURAL e RIBEIRINHA podem exigir licenciamento ambiental adicional. |

Usado em Community.community_type para definir regras de validacao especificas por tipo, determinar campos obrigatorios em formularios, filtrar relatorios por tipo de regularizacao, e gerar documentacao conforme legislacao aplicavel.
