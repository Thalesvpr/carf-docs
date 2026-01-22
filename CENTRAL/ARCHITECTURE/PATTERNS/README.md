---
type: readme
status: rejected
description: "Stub 8 linhas. Patterns devem ter contexto, problema, solucao, consequencias. Consolidar em ADR unico de arquitetura."
updated: 2026-01-15
---

# PATTERNS

Padrões arquiteturais aplicados no CARF, documentando quando usar cada um e seus trade-offs.

Os padrões de backend incluem [Clean Architecture](./01-clean-architecture.md) com camadas Domain, Application, Infrastructure e Gateway onde o domain fica no centro sem dependências externas. O [CQRS](./02-cqrs.md) separa comandos de escrita via MediatR de queries de leitura otimizadas. O [Repository com Unit of Work](./03-repository-uow.md) abstrai persistência e gerencia transações. E os [Domain Events](./04-domain-events.md) permitem comunicação entre bounded contexts.

Os padrões de frontend cobrem [composição de componentes React](./05-frontend-patterns.md) com custom hooks e gerenciamento de estado. O [offline-first mobile](./06-mobile-offline-first.md) define sincronização local-first com resolução de conflitos.

Os [padrões GIS](./07-gis-spatial-patterns.md) documentam uso de índices espaciais PostGIS, funções ST_*, formatos WKT/GeoJSON e validação de topologia.

## Padrões Documentados

### Backend (.NET)
- **[01-clean-architecture.md](./01-clean-architecture.md)** - Camadas e dependency inversion
- **[02-cqrs.md](./02-cqrs.md)** - Separação de commands e queries
- **[03-repository-uow.md](./03-repository-uow.md)** - Abstração de persistência
- **[04-domain-events.md](./04-domain-events.md)** - Comunicação entre bounded contexts

### Frontend (React/React Native)
- **[05-frontend-patterns.md](./05-frontend-patterns.md)** - Composição, hooks e state management
- **[06-mobile-offline-first.md](./06-mobile-offline-first.md)** - Sincronização e resolução de conflitos

### GIS/Spatial
- **[07-gis-spatial-patterns.md](./07-gis-spatial-patterns.md)** - PostGIS, índices espaciais e topologia


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (7 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-clean-architecture](./01-clean-architecture.md) | Clean Architecture |
| [02-cqrs](./02-cqrs.md) | CQRS |
| [03-repository-uow](./03-repository-uow.md) | Repository & Unit of Work |
| [04-domain-events](./04-domain-events.md) | Domain Events |
| [05-frontend-patterns](./05-frontend-patterns.md) | Frontend Patterns |
| [06-mobile-offline-first](./06-mobile-offline-first.md) | Mobile Offline-First |
| [07-gis-spatial-patterns](./07-gis-spatial-patterns.md) | GIS Spatial Patterns |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/01-clean-architecture.md|Clean Architecture]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/02-cqrs.md|CQRS]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/03-repository-uow.md|Repository & Unit of Work]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/04-domain-events.md|Domain Events]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md|Frontend Patterns]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/06-mobile-offline-first.md|Mobile Offline-First]]
- ○ [[CENTRAL/ARCHITECTURE/PATTERNS/07-gis-spatial-patterns.md|GIS Spatial Patterns]]

<!-- CARF-INDEX-END -->
