---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-084: Criar Titular

## Descricao

Sistema deve permitir cadastro de novos titulares representando pessoas fisicas ou juridicas responsaveis por unidades habitacionais. Formulario captura nome completo ou razao social, CPF ou CNPJ conforme tipo de pessoa, e informacoes de contato. Validacao de CPF e CNPJ utiliza algoritmo de verificacao de digitos. Sistema verifica duplicidade por CPF/CNPJ antes de permitir criacao, alertando quando documento ja existe e oferecendo vincular titular existente. Conforme WORKFLOW-MESTRE, equipe de campo (Coordenador e Cadastrador) cadastra titulares durante coleta em campo via REURBCAD.

## Criterios de Aceitacao

1. Formulario com campos obrigatorios por tipo de pessoa
2. Validacao algoritmica de CPF e CNPJ
3. Verificacao de duplicidade antes de criar
4. Opcao de vincular titular existente se duplicado
5. Suporte a pessoa fisica e juridica

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-088, RF-089, RF-090, RF-096
