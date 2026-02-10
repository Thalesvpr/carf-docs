---
type: leaf
status: review
updated: 2026-02-08
---

# EntityType

Value object enum imutavel representando o tipo de entidade pai em relacionamentos polimorficos. Utilizado nas tabelas documents e annotations para identificar a entidade a que o registro esta vinculado via par (entity_type, entity_id). Tambem usado em audit_logs para rastrear mudancas em qualquer entidade do dominio.

## Valores Permitidos

| Valor | Descricao | Uso |
|-------|-----------|-----|
| UNIT | Unidade habitacional | Documents, Annotations e AuditLogs vinculados a units. |
| HOLDER | Titular ou posseiro | Documents pessoais (RG, CPF, comprovantes) e AuditLogs. |
| COMMUNITY | Comunidade | Documents, Annotations e AuditLogs de nivel comunitario. |
| BLOCK | Quadra urbana | AuditLogs rastreando mudancas em quadras. |
| PLOT | Lote individual | AuditLogs rastreando mudancas em lotes. |

## Uso no Dominio

EntityType determina qual tabela contem a entidade pai referenciada por entity_id. Indice composto em (entity_type, entity_id) nas tabelas documents e annotations acelera listagem de anexos e anotacoes de uma entidade. Em audit_logs, o escopo e mais amplo incluindo BLOCK e PLOT para rastreamento completo de todas operacoes de escrita no sistema.
