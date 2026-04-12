---
type: leaf
status: rejected
updated: 2026-02-08
description: Propriedades IsResolved, ResolvedAt, ResolvedBy, DueDate e AuthorId nao existem na tabela annotations do schema PostgreSQL. Schema define apenas id, tenant_id, entity_type, entity_id, annotation_type, content, priority, created_at, created_by, deleted_at.
---

# Annotation

Entidade representando uma anotacao ou observacao vinculada polimorficamente a qualquer entidade do sistema, permitindo registro de notas, alertas, problemas e lembretes com rastreamento de resolucao e prazos. Herda de BaseEntity fornecendo auditoria temporal e soft delete. Mapeada para a tabela annotations no banco de dados.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| EntityType | EntityType | nao | Tipo da entidade anotada (UNIT, HOLDER, COMMUNITY). Determina o contexto da anotacao. |
| EntityId | Guid | nao | ID da entidade pai. Junto com EntityType forma a referencia polimorfica. |
| AuthorId | Guid | nao | FK para Account do autor. Mapeado para created_by no banco. |
| Content | string | nao | Texto da anotacao. Suporta formato livre. |
| AnnotationType | AnnotationType | nao | Tipo da anotacao: NOTE, WARNING, ISSUE, REMINDER. Determina comportamento e visualizacao. |
| Priority | Priority? | sim | LOW, NORMAL, HIGH, URGENT. Obrigatorio quando AnnotationType e ISSUE ou REMINDER. |
| IsResolved | bool | nao | Aplicavel a ISSUE. Indica se o problema foi solucionado. Default false. |
| ResolvedAt | DateTime? | sim | Timestamp de quando o ISSUE foi resolvido. |
| ResolvedBy | Guid? | sim | FK para Account que resolveu o ISSUE. |
| DueDate | DateTime? | sim | Prazo limite. Obrigatorio para REMINDER. |

## Metodos

| Metodo | Descricao |
|--------|-----------|
| Resolve(accountId) | Marca ISSUE como resolvido preenchendo IsResolved, ResolvedAt e ResolvedBy. Valida que AnnotationType e ISSUE. |
| Unresolve() | Reabre um ISSUE previamente resolvido, limpando campos de resolucao. |
| UpdateContent(newContent) | Atualiza o texto da anotacao, chamando Touch() para atualizar timestamp. |
| IsOverdue() | Retorna true se AnnotationType e REMINDER e DueDate ja passou. |

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Priority obrigatorio | Priority deve ser preenchido quando AnnotationType e ISSUE ou REMINDER. |
| DueDate obrigatorio | DueDate deve ser preenchido quando AnnotationType e REMINDER. |
| Resolve apenas ISSUE | Metodo Resolve so pode ser chamado em anotacoes do tipo ISSUE. |
| Content obrigatorio | Content nao pode ser vazio ou nulo. |

## Eventos de Dominio

Annotation nao e aggregate root, portanto seus eventos sao despachados pelo agregado pai. Ao criar uma anotacao do tipo ISSUE com prioridade HIGH ou URGENT, o sistema agenda verificacao de prazo via Hangfire. Anotacoes do tipo REMINDER com DueDate proximo disparam notificacao push para o autor.
