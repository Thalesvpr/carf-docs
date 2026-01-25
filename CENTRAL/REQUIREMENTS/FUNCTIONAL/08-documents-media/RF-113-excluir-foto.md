---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-113: Excluir Foto

## Descricao

Sistema deve permitir exclusao de fotos via soft delete marcando registro como excluido sem remocao fisica imediata. Confirmacao explicita obrigatoria previne remocoes acidentais. Apos confirmacao, sistema programa remocao do arquivo fisico no storage S3/MinIO liberando espaco mas mantendo registro de metadados para auditoria. Log de auditoria registra usuario, timestamp, identificador e contexto. Interface remove foto imediatamente da galeria apos exclusao bem-sucedida.

## Criterios de Aceitacao

1. Soft delete preservando metadados
2. Confirmacao explicita obrigatoria
3. Remocao programada do arquivo fisico
4. Log de auditoria completo
5. Atualizacao imediata da galeria

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-108, RF-116
