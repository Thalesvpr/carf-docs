# RELATIONSHIPS - Relacionamentos Entre Entidades

Documentação detalhada de relacionamentos entre entidades do domínio CARF especificando cardinalidade foreign keys constraints de integridade relacionamentos polimórficos e navegação bidirecional.

## Documentação

- **[entity-relationships.md](./entity-relationships.md)** - Mapeamento completo de todos relacionamentos entre entidades (1:1, 1:N, N:N)

## Tipos de Relacionamentos

### One-to-Many (1:N)
Relacionamentos onde uma entidade pai possui múltiplas entidades filhas (ex: Community → Units, Unit → Documents).

### Many-to-Many (N:N)
Relacionamentos N:N com tabela de junção (ex: Unit ↔ Holder via UnitHolder, Account ↔ Team via TeamMember).

### Polymorphic
Relacionamentos polimórficos onde entidade pode referenciar múltiplos tipos (ex: Document → entity_type + entity_id referencia Unit, Holder, Community, etc.).

### Self-Referencing
Relacionamentos recursivos onde entidade referencia a si mesma (ex: Block → parent_block_id para hierarquia).

## Princípios de Design

**Aggregate Boundaries:** Relacionamentos entre aggregates são apenas por ID, não por objeto completo.

**Bidirectional Navigation:** Quando necessária navegação bidirecional, documentar owner side e inverse side.

**Cascade Delete:** Especificar comportamento de cascade para deletes (CASCADE, SET NULL, RESTRICT).

**Foreign Key Constraints:** Garantir integridade referencial via database constraints.

Ver também:
- **[ENTITIES/](../ENTITIES/README.md)** - Definições de entidades
- **[AGGREGATES/](../AGGREGATES/README.md)** - Fronteiras de agregados
- **[DIAGRAMS/](../DIAGRAMS/README.md)** - Visualizações gráficas

---

**Última atualização:** 2026-01-10
