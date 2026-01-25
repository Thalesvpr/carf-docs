---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-089: Campos de Pessoa Fisica

## Descricao

Sistema deve capturar campos para titulares PESSOA_FISICA incluindo nome completo, CPF validado, RG com orgao emissor e UF, data de nascimento, genero e estado civil (SOLTEIRO, CASADO, DIVORCIADO, VIUVO, UNIAO_ESTAVEL), alem de telefone e email. Validacao de CPF utiliza algoritmo de verificacao de digitos verificadores. Email validado via regex. Telefone formatado automaticamente com mascara adequada. Campos essenciais para identificacao e comunicacao com beneficiarios de regularizacao fundiaria.

## Criterios de Aceitacao

1. Campos: nome, CPF, RG, nascimento, genero, estado civil
2. Validacao algoritmica de CPF
3. Validacao de formato de email
4. Mascara automatica para telefone
5. Estado civil como enum predefinido

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-088, RF-096
