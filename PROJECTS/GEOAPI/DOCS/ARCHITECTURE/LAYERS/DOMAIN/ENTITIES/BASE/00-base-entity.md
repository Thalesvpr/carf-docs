---
type: leaf
status: review
updated: 2026-02-08
---

# BaseEntity

Classe base abstrata que todas as entidades de dominio herdam, fornecendo campos comuns de auditoria, rastreamento temporal e soft delete. Toda entidade no sistema (Unit, Holder, Community, Team, Document, Annotation) estende BaseEntity garantindo consistencia de metadados e comportamentos transversais em todo o dominio.

## Propriedades

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico gerado na criacao. Imutavel apos criacao. Mapeado para coluna uuid com gen_random_uuid(). |
| CreatedAt | DateTime | Timestamp automatico no momento da criacao. Nao pode ser alterado posteriormente. |
| UpdatedAt | DateTime | Timestamp da ultima alteracao, atualizado automaticamente pelo metodo Touch(). |
| CreatedBy | Guid | UUID da Account que criou o registro. Populado automaticamente via ICurrentUser. |
| UpdatedBy | Guid | UUID da Account que realizou a ultima alteracao. Atualizado junto com UpdatedAt. |
| DeletedAt | DateTime? | Nullable. Null indica registro ativo. Preenchido pelo SoftDelete() sem remover fisicamente o registro do banco, permitindo recuperacao e compliance LGPD. |
| Version | int | Controle de concorrencia otimista. Mapeado para coluna version (int) no PostgreSQL, incrementado a cada UPDATE. EF Core compara version lido com version atual ao salvar, lancando ConflictException se divergirem. |

## Metodos

| Metodo | Retorno | Descricao |
|--------|---------|-----------|
| Touch() | void | Atualiza UpdatedAt para o momento atual. Chamado internamente por todo metodo que altera estado da entidade. |
| SoftDelete() | void | Preenche DeletedAt com o momento atual. O registro permanece no banco mas e filtrado por queries padrao via filtro global deleted_at IS NULL. |
| IsDeleted | bool | Propriedade calculada que retorna true se DeletedAt nao e null. |

## Convencoes de Auditoria

Todas as tabelas mapeadas a partir de BaseEntity possuem indices parciais em deleted_at IS NULL para excluir registros soft-deleted das queries padrao. O campo Version e mapeado para coluna version do tipo int no PostgreSQL, incrementado a cada UPDATE via trigger. EF Core detecta conflitos de concorrencia comparando o version lido com o version atual do banco ao salvar mudancas. CreatedBy e UpdatedBy sao populados automaticamente via interceptor que consulta ICurrentUser.

Propriedades Now e Today podem ser injetadas via IDateTimeProvider, permitindo testes unitarios com datas fixas sem depender do relogio do sistema.
