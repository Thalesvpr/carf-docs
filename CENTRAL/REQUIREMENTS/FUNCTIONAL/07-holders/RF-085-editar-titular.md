---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-085: Editar Titular

## Descricao

Sistema deve permitir edicao de dados cadastrais de titulares existentes. Interface oferece formulario preenchido com valores atuais possibilitando atualizacao de qualquer campo. Todas alteracoes registradas em log de auditoria com timestamp, usuario, campos modificados e valores anteriores e novos. Mesmas validacoes de criacao sao reaplicadas incluindo verificacao de CPF/CNPJ e duplicidade se documento for alterado. Edicao essencial para correcao de erros, atualizacao de contatos e complementacao de dados.

## Criterios de Aceitacao

1. Formulario preenchido com valores atuais
2. Validacoes reaplicadas na edicao
3. Log de auditoria com valores anteriores
4. Verificacao de duplicidade se documento alterado
5. Suporte a edicao de todos os campos

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-084, RF-096
