---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-088: Tipos de Titular

## Descricao

Sistema deve suportar categorizacao de titulares em tipos PESSOA_FISICA e PESSOA_JURIDICA atraves de enumeracao que garante valores consistentes. Quando tipo e PESSOA_FISICA, formulario exibe campos como CPF, RG, data de nascimento e estado civil. Quando tipo e PESSOA_JURIDICA, formulario apresenta campos como CNPJ, razao social, nome fantasia e representante legal. Validacao de documento aplicada condicionalmente baseada no tipo selecionado.

## Criterios de Aceitacao

1. Enum com PESSOA_FISICA e PESSOA_JURIDICA
2. Renderizacao condicional de campos por tipo
3. Validacao de CPF para pessoa fisica
4. Validacao de CNPJ para pessoa juridica
5. Campos especificos ocultos quando nao aplicaveis

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-084, RF-089, RF-090
