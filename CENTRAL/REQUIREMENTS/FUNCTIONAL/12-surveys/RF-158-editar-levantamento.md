---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-158: Editar Levantamento

## Descricao

Sistema deve permitir edicao de dados de levantamentos topograficos existentes para correcao de metadados e atualizacao de arquivos. Atualizacao de campos descritivos incluindo data, responsavel tecnico, equipamento e vinculacao a comunidade, com formulario populado com valores atuais para modificacao. Suporte a re-upload de arquivos brutos permitindo substituir arquivo original por versao corrigida ou adicionar como versao adicional conforme versionamento. Alteracoes geram entradas no log de auditoria registrando usuario, timestamp, campos modificados e valores anteriores versus novos. Sistema valida dados editados garantindo consistencia e integridade antes de persistir.

## Criterios de Aceitacao

1. Edicao de todos campos descritivos
2. Re-upload de arquivos com versionamento
3. Log de auditoria com diff de valores
4. Validacao de consistencia
5. Formulario populado com valores atuais

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-157, RF-120
