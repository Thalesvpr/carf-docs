---
type: readme
status: rejected
description: "Estrutura caotica. Numeracao nao agrupa por categoria. Precisa reorganizar por agregado/contexto."
updated: 2026-01-15
---

# RELATIONSHIPS

Relacionamentos entre entidades do domínio CARF, especificando cardinalidades, foreign keys e constraints de integridade referencial.

Relacionamentos entre aggregates diferentes usam apenas IDs, nunca referências diretas a objetos, garantindo fronteiras transacionais claras conforme padrões DDD. Inclui relacionamentos auto-referenciados hierárquicos e cascade delete behaviors definidos nas constraints do PostgreSQL.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (1 arquivo)

| ID | Titulo |
|:---|:-------|
| [01-entity-relationships](./01-entity-relationships.md) | Entity Relationships |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (1)

| Documento | Status |
|-----------|--------|
| [Entity Relationships](./01-entity-relationships.md) | ○ |

<!-- CARF-INDEX-END -->
