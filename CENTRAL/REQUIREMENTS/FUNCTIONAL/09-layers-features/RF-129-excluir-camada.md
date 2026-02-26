---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-129: Excluir Camada

## Descricao

Sistema deve permitir exclusao de camadas GIS atraves de processo controlado que garante integridade de dados e previne remocoes acidentais, implementado via soft delete. Antes de permitir exclusao, sistema verifica se existem features vinculadas, apresentando aviso com quantidade de features afetadas e solicitando confirmacao explicita. Soft delete atraves de campo deleted_at marca camada como excluida preservando dados para auditoria e recuperacao. Camadas soft-deleted nao aparecem em listagens normais mas podem ser acessadas por interfaces administrativas. Exclusao exige confirmacao adicional via dialogo. Operacao registrada no log de auditoria com identificacao do administrador, timestamp e contexto.

## Criterios de Aceitacao

1. Soft delete com campo deleted_at
2. Verificacao de features vinculadas
3. Confirmacao explicita antes de excluir
4. Ocultacao de listagens normais
5. Registro em log de auditoria

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-132
