---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-090: Campos de Pessoa Juridica

## Descricao

Sistema deve capturar campos para titulares PESSOA_JURIDICA incluindo razao social, nome fantasia, CNPJ validado, inscricao estadual e representante legal obrigatorio. Validacao de CNPJ utiliza algoritmo especifico de verificacao de digitos. Campos especificos exibidos dinamicamente apenas quando tipo PESSOA_JURIDICA selecionado. Representante legal obrigatorio garante identificacao de responsavel para comunicacao. Campos essenciais para cadastro de empresas, cooperativas e associacoes titulares de unidades.

## Criterios de Aceitacao

1. Campos: razao social, nome fantasia, CNPJ, inscricao estadual
2. Representante legal obrigatorio
3. Validacao algoritmica de CNPJ
4. Exibicao condicional por tipo de titular
5. Inscricao estadual opcional

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-088, RF-096
