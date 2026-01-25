---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-107: Excluir Documento

## Descricao

Sistema deve permitir que usuarios autorizados excluam documentos via soft delete marcando registro como inativo sem remocao fisica imediata. Confirmacao obrigatoria previne remocoes acidentais atraves de modal solicitando confirmacao explicita com opcao de informar razao. Toda exclusao gera registro no log de auditoria com usuario, timestamp, identificador e contexto. Documento nao aparece mais nas listagens mas permanece para auditoria. Endpoint DELETE com validacao de permissoes.

## Criterios de Aceitacao

1. Soft delete preservando registro
2. Modal de confirmacao obrigatoria
3. Log de auditoria completo
4. Opcao de informar razao da exclusao
5. Remocao da listagem apos exclusao

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-102, RF-105
