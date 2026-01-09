# Arquitetura

Visão geral da arquitetura do sistema CARF.

## Arquitetura Polyrepo

O CARF segue arquitetura **polyrepo** com 6 repositórios Git independentes:

```
┌─────────────────────────────────────────────────────┐
│              carf-docs (Documentação)               │
│                Single Source of Truth               │
└─────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌──────▼─────┐  ┌──────▼─────┐
    │ carf-geoapi│  │carf-geoweb │  │carf-reurbcad│
    │ Backend    │  │ Frontend   │  │  Mobile    │
    │ .NET 9     │  │  React     │  │React Native│
    └────────────┘  └────────────┘  └────────────┘
           │               │
    ┌──────▼─────┐  ┌──────▼─────┐
    │carf-geogis │  │carf-webdocs│
    │Plugin QGIS │  │Docs Portal │
    │  Python    │  │ VitePress  │
    └────────────┘  └────────────┘
```

## Stack Tecnológica

### Backend (GEOAPI)

- **.NET 9** - Framework principal
- **Clean Architecture** - Separação de responsabilidades
- **CQRS** - Command Query Responsibility Segregation
- **DDD** - Domain-Driven Design
- **Entity Framework Core** - ORM
- **PostgreSQL 16 + PostGIS** - Banco de dados geoespacial
- **Keycloak** - OAuth2/OIDC autenticação

### Frontend Web (GEOWEB)

- **React 18** - Framework UI
- **TypeScript** - Tipagem estática
- **Feature-Sliced Design** - Arquitetura modular
- **React Query** - Cache e sincronização
- **React Router v6** - Navegação
- **Zustand** - State management
- **Tailwind CSS** - Estilização

### Mobile (REURBCAD)

- **React Native** - Framework mobile
- **TypeScript** - Tipagem estática
- **WatermelonDB** - Banco local SQLite
- **Offline-First** - Estratégia de sincronização
- **React Navigation v6** - Navegação
- **Geolocalização** - GPS tracking

### Plugin GIS (GEOGIS)

- **Python 3.x** - Linguagem principal
- **PyQGIS API** - Integração QGIS
- **Shapefile/GeoJSON** - Formatos de exportação

### Docs (WEBDOCS)

- **VitePress** - Static site generator
- **Vue 3** - Framework UI
- **Markdown** - Formato de documentação

## Padrões Arquiteturais

### Clean Architecture (GEOAPI)

```
┌─────────────────────────────────────┐
│          Gateway (API)              │
│  Controllers, Middlewares, Filters  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        Infrastructure               │
│  EF Core, PostgreSQL, Keycloak      │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         Application                 │
│  Use Cases (Commands/Queries)       │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│           Domain                    │
│  Entities, Value Objects, Events    │
└─────────────────────────────────────┘
```

### Feature-Sliced Design (GEOWEB)

```
src/
├── app/          # Providers, Router
├── features/     # Módulos isolados
│   ├── auth/
│   ├── units/
│   ├── holders/
│   └── communities/
├── entities/     # Modelos de domínio
└── shared/       # Componentes reutilizáveis
```

## Multi-Tenancy

Row-Level Security (RLS) do PostgreSQL garante isolamento automático por `tenant_id`:

```sql
CREATE POLICY tenant_isolation ON units
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Segurança

- **OAuth2/OIDC** via Keycloak
- **Row-Level Security** no PostgreSQL
- **HTTPS** obrigatório em produção
- **CORS** configurado por ambiente
- **Rate Limiting** para APIs públicas

## Documentação Detalhada

- [ADRs](https://github.com/Thalesvpr/carf-docs/tree/main/CENTRAL/ARCHITECTURE/ADRs)
- [Deployment](https://github.com/Thalesvpr/carf-docs/tree/main/CENTRAL/ARCHITECTURE/DEPLOYMENT)
- [Patterns](https://github.com/Thalesvpr/carf-docs/tree/main/CENTRAL/ARCHITECTURE/PATTERNS)

## Próximos Passos

- Ver [Requisitos](/requisitos/)
- Consultar [API](/api/)
- Explorar [Funcionalidades](/funcionalidades/)
