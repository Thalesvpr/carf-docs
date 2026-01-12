# RELATIONSHIPS

Relacionamentos entre entidades domínio CARF especificando cardinalidade foreign keys constraints integridade referencial relacionamentos polimórficos navegação bidirecional entre objetos mapeando como Unit Holder Community Document e demais 33 entities se associam via one-to-many one-to-one many-to-many relationships respeitando aggregate boundaries onde relacionamentos entre aggregates diferentes usam apenas IDs nunca referências diretas a objetos garantindo boundaries transacionais claros conforme padrões DDD tactical design incluindo relacionamentos auto-referenciados hierárquicos como Block parent_block_id UnitAddress parent_address_id cascade delete behaviors CASCADE SET NULL RESTRICT definidos database constraints PostgreSQL.

## Documentos

- **[entity-relationships.md](./entity-relationships.md)** - Mapeamento completo relacionamentos entidades cardinalidades constraints

---

**Última atualização:** 2026-01-11
