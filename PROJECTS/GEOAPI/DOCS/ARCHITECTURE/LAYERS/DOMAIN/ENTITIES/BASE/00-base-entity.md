# BaseEntity

Classe base abstrata que todas entidades domínio herdam fornecendo campos comuns e comportamentos essenciais para auditoria rastreamento temporal e soft delete. Campos incluem Id Guid gerado criação e imutável como identificador único, CreatedAt DateTime automático criação, UpdatedAt DateTime última alteração, DeletedAt DateTime nullable para soft delete null se ativo e RowVersion byte array para controle concorrência otimista evitando conflitos via EF Core.

Métodos principais são Touch() atualizando UpdatedAt para momento atual chamado em todo método que altera entidade, SoftDelete() marcando entidade como excluída preenchendo DeletedAt sem deletar fisicamente banco permitindo recuperação compliance LGPD, e propriedades Now/Today retornando data/hora atual injetáveis via IDateTimeProvider permitindo testes com datas fixas. Todas entities do sistema (Unit, Holder, Community, Team) herdam desta classe garantindo consistência auditoria rastreabilidade temporal todo domínio.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
