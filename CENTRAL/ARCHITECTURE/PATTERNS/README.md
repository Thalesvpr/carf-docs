# PATTERNS

Padrões arquiteturais aplicados no CARF documentando Clean Architecture (camadas Domain/Application/Infrastructure/Gateway com dependency inversion, domain no centro sem dependências externas), CQRS (Command Query Responsibility Segregation separando writes commands via MediatR de reads queries otimizadas com Dapper), Repository Pattern (abstração de persistência com interfaces IUnitRepository, IHolderRepository implementadas por EF Core), Unit of Work (gerenciamento transacional coordenando múltiplos repositories em transação única), Domain Events (eventos disparados por aggregates para comunicação entre bounded contexts mantendo consistência eventual), Specification Pattern (encapsular regras de filtro complexas reutilizáveis), Factory Pattern (criar aggregates complexos com validações), e Strategy Pattern (múltiplas estratégias de cálculo de área, validação de documentos). Define quando aplicar cada pattern e trade-offs.

---

**Última atualização:** 2025-12-29
