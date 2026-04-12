---
type: leaf
status: review
updated: 2026-02-08
---

# EntityType

Value object enum representando tipo de entidade em contextos polimorficos onde multiplas entidades podem ser referenciadas pelo mesmo campo, permitindo relacionamentos genericos mantendo type-safety. No banco de dados, usado em annotations.entity_type, documents.entity_type e audit_logs.entity_type (varchar(30)).

O EntityType permite que tabelas como documents e annotations vinculem-se a qualquer entidade do dominio via combinacao entity_type + entity_id, implementando padrao polimorfico sem heranca de tabela. A tabela documents define CHECK constraint limitando entity_type aos valores UNIT, HOLDER e COMMUNITY, porem audit_logs aceita qualquer tipo incluindo BLOCK e PLOT para rastreamento completo de mudancas.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| UNIT | Unidade habitacional cadastrada. Principal entidade do dominio. |
| HOLDER | Titular pessoa fisica ou juridica vinculado a unidades. |
| COMMUNITY | Comunidade ou assentamento agrupando unidades. |
| BLOCK | Quadra urbana subdividindo uma comunidade. Usado em audit_logs. |
| PLOT | Lote individual dentro de um bloco. Usado em audit_logs. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Tipo valido | Deve ser um dos valores permitidos no contexto de uso. Documents e annotations aceitam UNIT, HOLDER e COMMUNITY. Audit logs aceitam todos os valores. |
| Entidade existente | O entity_id deve referenciar registro existente do tipo indicado na tabela correspondente. |
| Consistencia | O tipo deve corresponder a tabela correta para queries de integridade referencial. |

Usado em Annotation.entity_type e Document.entity_type criando relacionamento polimorfico permitindo anotar ou anexar documentos a qualquer entidade, em AuditLog.entity_type rastreando mudancas em todas entidades do dominio, e em queries genericas agregando resultados por tipo para relatorios e dashboards.
