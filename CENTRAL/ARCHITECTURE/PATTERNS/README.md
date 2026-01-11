# PATTERNS

Padrões arquiteturais aplicados no CARF documentando Clean Architecture (camadas Domain/Application/Infrastructure/Gateway com dependency inversion, domain no centro sem dependências externas), CQRS (Command Query Responsibility Segregation separando writes commands via MediatR de reads queries otimizadas com Dapper), Repository Pattern (abstração de persistência com interfaces IUnitRepository, IHolderRepository implementadas por EF Core), Unit of Work (gerenciamento transacional coordenando múltiplos repositories em transação única), Domain Events (eventos disparados por aggregates para comunicação entre bounded contexts mantendo consistência eventual), Specification Pattern (encapsular regras de filtro complexas reutilizáveis), Factory Pattern (criar aggregates complexos com validações), e Strategy Pattern (múltiplas estratégias de cálculo de área, validação de documentos). Define quando aplicar cada pattern e trade-offs.

## Padrões Documentados

### Backend Patterns (.NET)
- **[01-clean-architecture.md](./01-clean-architecture.md)** - Clean Architecture com camadas Domain/Application/Infrastructure/Gateway, dependency inversion, domain independente
- **[02-cqrs.md](./02-cqrs.md)** - Command Query Responsibility Segregation separando writes (MediatR commands) de reads (queries otimizadas)
- **[03-repository-uow.md](./03-repository-uow.md)** - Repository Pattern + Unit of Work para abstração de persistência e gerenciamento transacional
- **[04-domain-events.md](./04-domain-events.md)** - Domain Events para comunicação entre bounded contexts mantendo consistência eventual

### Frontend Patterns (React/React Native)
- **[05-frontend-patterns.md](./05-frontend-patterns.md)** - Padrões React (Component composition, Custom hooks, Context API, State management)
- **[06-mobile-offline-first.md](./06-mobile-offline-first.md)** - Offline-first architecture para React Native com sincronização local-first e conflict resolution

### GIS/Spatial Patterns
- **[07-gis-spatial-patterns.md](./07-gis-spatial-patterns.md)** - Padrões geoespaciais PostGIS (Spatial indexes, ST_* functions, WKT/GeoJSON, topology validation)

---

**Última atualização:** 2025-12-29
