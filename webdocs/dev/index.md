---
layout: home

hero:
  name: Documentação CARF
  text: Área Desenvolvedores
  tagline: Arquitetura, API, setup e guias técnicos
  actions:
    - theme: brand
      text: Setup Inicial
      link: /dev/setup/
    - theme: alt
      text: API Reference
      link: /dev/api/

features:
  - icon: 🚀
    title: Setup & Getting Started
    details: Configure seu ambiente de desenvolvimento
    link: /dev/setup/
  - icon: 🏗️
    title: Arquitetura
    details: Clean Architecture, CQRS, DDD e patterns
    link: /dev/arquitetura/
  - icon: 🔌
    title: API Reference
    details: Endpoints REST, contratos e exemplos
    link: /dev/api/
  - icon: 🗄️
    title: Database
    details: Schema, migrations, RLS policies
    link: /dev/database/
  - icon: 📚
    title: Guias Técnicos
    details: How-to, best practices e troubleshooting
    link: /dev/guias/
  - icon: 📋
    title: Ver Requisitos
    details: Acesso completo aos requisitos funcionais
    link: /docs/requisitos/
---

## Bem-vindo à Documentação Técnica

Esta área contém toda a documentação voltada para **Desenvolvedores**, **Arquitetos** e **DevOps**.

### O que você encontra aqui:

- **Setup & Getting Started**: Configure ambiente local, clone repos, rode projetos
- **Arquitetura**: Clean Architecture, CQRS, DDD, multi-tenancy, polyrepo strategy
- **API Reference**: Todos os endpoints REST com exemplos e contratos
- **Database**: Schema PostgreSQL + PostGIS, migrations, RLS policies
- **Guias Técnicos**: How-to guides, best practices, troubleshooting

### Navegação por Projeto

#### Backend (GEOAPI - .NET 9)
- [Setup Backend](/dev/setup/#backend-geoapi)
- [Arquitetura Clean](/dev/arquitetura/#clean-architecture)
- [Database & RLS](/dev/database/)
- [API Endpoints](/dev/api/)

#### Frontend (GEOWEB - React)
- [Setup Frontend](/dev/setup/#frontend-geoweb)
- [Feature-Sliced Design](/dev/arquitetura/#feature-sliced-design)
- [Integração API](/dev/guias/integracao-api)

#### Mobile (REURBCAD - React Native)
- [Setup Mobile](/dev/setup/#mobile-reurbcad)
- [Offline-First](/dev/arquitetura/#offline-first)
- [Sincronização](/dev/guias/sincronizacao)

#### Plugin GIS (GEOGIS - QGIS Python)
- [Setup Plugin](/dev/setup/#plugin-geogis)
- [PyQGIS API](/dev/guias/pyqgis)

### Stack Tecnológica

| Componente | Stack |
|------------|-------|
| **Backend** | .NET 9, EF Core, PostgreSQL + PostGIS, Keycloak |
| **Frontend** | React 18, TypeScript, React Query, Zustand |
| **Mobile** | React Native, WatermelonDB, Offline-First |
| **Plugin** | Python 3.x, PyQGIS API |
| **Docs** | VitePress, Vue 3 |

---

**Product Owner?** Acesse a [Documentação de Negócio](/docs/) para requisitos, funcionalidades e roadmap.
