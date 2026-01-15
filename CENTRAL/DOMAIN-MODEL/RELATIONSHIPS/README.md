# RELATIONSHIPS

Relacionamentos entre entidades do domínio CARF, especificando cardinalidades, foreign keys e constraints de integridade referencial.

Relacionamentos entre aggregates diferentes usam apenas IDs, nunca referências diretas a objetos, garantindo fronteiras transacionais claras conforme padrões DDD. Inclui relacionamentos auto-referenciados hierárquicos e cascade delete behaviors definidos nas constraints do PostgreSQL.

## Documentos

- **[entity-relationships.md](./entity-relationships.md)** - Mapeamento completo de relacionamentos e cardinalidades

---

**Última atualização:** 2026-01-14
