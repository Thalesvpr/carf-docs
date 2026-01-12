# ENTITIES

Entidades de domínio do GEOAPI encapsulando lógica e regras de negócio organizadas por features do sistema. Todas herdam de BaseEntity fornecendo Id Guid imutável, timestamps CreatedAt/UpdatedAt, DeletedAt para soft delete e RowVersion para controle de concorrência otimista, ou de BaseAggregateRoot que adiciona suporte a domain events despachados após SaveChanges para notificações e workflows assíncronos. Organizadas em catorze categorias cobrindo desde autenticação e multi-tenancy até workflow de legitimação fundiária, GIS layers, topografia e auditoria, cada entity encapsula invariants e comportamentos garantindo que estado permanece consistente através de métodos públicos que validam pré-condições antes de alterar campos privados evitando anemic domain model.

## Categorias

- **[BASE/](./BASE/README.md)** - Classes base para todas entities e aggregate roots
- **[AUTH/](./AUTH/README.md)** - Autenticação sessões e API keys
- **[CORE/](./CORE/README.md)** - Accounts e tenants multi-tenancy
- **[TEAMS/](./TEAMS/README.md)** - Equipes técnicas e autorizações comunidades
- **[COMMUNITIES/](./COMMUNITIES/README.md)** - Comunidades blocks plots organização espacial
- **[UNITS/](./UNITS/README.md)** - Unidades habitacionais aggregate root central
- **[HOLDERS/](./HOLDERS/README.md)** - Titulares e relacionamentos com units
- **[DOCUMENTS/](./DOCUMENTS/README.md)** - Documentos anexos arquivos
- **[GIS/](./GIS/README.md)** - Layers features WMS servers serviços GIS
- **[SURVEYING/](./SURVEYING/README.md)** - Topografia surveyor RBMC processamento
- **[LEGITIMATION/](./LEGITIMATION/README.md)** - Workflow legitimação fundiária Lei 13465/2017
- **[ANNOTATIONS/](./ANNOTATIONS/README.md)** - Anotações comentários colaborativos
- **[SYNC/](./SYNC/README.md)** - Sincronização mobile detecção conflitos
- **[AUDIT/](./AUDIT/README.md)** - Auditoria logs operações críticas

---

**Última atualização:** 2026-01-12
