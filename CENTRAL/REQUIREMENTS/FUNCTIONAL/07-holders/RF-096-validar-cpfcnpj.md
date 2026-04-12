---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-096: Validar CPF/CNPJ

## Descricao

Sistema deve implementar validacao algoritmica de CPF e CNPJ atraves de verificacao de digitos verificadores conforme regras matematicas da Receita Federal. Calculo de modulo 11 aplicado aos digitos base gera e compara digitos verificadores. Validacao ocorre no backend garantindo seguranca e replicada no frontend para feedback imediato. Mensagem de erro clara quando documento invalido. Rejeicao automatica de sequencias invalidas como numeros repetidos (111.111.111-11).

## Criterios de Aceitacao

1. Algoritmo de modulo 11 para CPF e CNPJ
2. Validacao server-side e client-side
3. Mensagem de erro especifica
4. Rejeicao de sequencias invalidas
5. Diferenciacao de tipos de erro

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-089, RF-090, RF-084
