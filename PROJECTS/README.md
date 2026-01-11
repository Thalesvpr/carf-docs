# PROJECTS - Aplicações e Bibliotecas

Implementações técnicas do sistema CARF organizadas em 6 aplicações principais e 3 bibliotecas TypeScript compartilhadas seguindo decisões arquiteturais documentadas em [CENTRAL/ARCHITECTURE](../CENTRAL/ARCHITECTURE/README.md) e implementando [domain model](../CENTRAL/DOMAIN-MODEL/00-INDEX.md) unificado conforme [ADRs](../CENTRAL/ARCHITECTURE/ADRs/ADR-001-dotnet-9-backend.md) registrando escolhas tecnológicas e trade-offs.

Backend e infraestrutura implementados via GEOAPI API REST .NET 9 + PostgreSQL/PostGIS e [KEYCLOAK](./KEYCLOAK/README.md) provendo autenticação OAuth2/OIDC SSO centralizado. Aplicações frontend web incluem [GEOWEB](./GEOWEB/DOCS/README.md) portal React + Vite para gestão geoespacial e [ADMIN](./ADMIN/DOCS/README.md) console administrativo também React + Vite, além de [WEBDOCS](./WEBDOCS/DOCS/README.md) site VitePress para documentação técnica.

Aplicações mobile e GIS desktop compreendem [REURBCAD](./REURBCAD/DOCS/README.md) app React Native offline-first para coleta campo e [GEOGIS](./GEOGIS/DOCS/README.md) plugin Python QGIS para análises espaciais avançadas.

## Aplicações

### [GEOAPI](./GEOAPI/DOCS/README.md) - Backend REST API .NET
Backend API REST .NET 9 implementando Clean Architecture + DDD com PostgreSQL+PostGIS, endpoints CRUD de unidades/comunidades/titulares/legitimação, autenticação OAuth2 Keycloak JWT, multi-tenancy via RLS, CQRS MediatR, background jobs Hangfire.

**Stack:** .NET 9, ASP.NET Core, Entity Framework Core, PostgreSQL+PostGIS, Keycloak, MediatR, FluentValidation, Hangfire

### [GEOWEB](./GEOWEB/DOCS/README.md) - Portal Web Geoespacial
Portal web React para gestão de unidades habitacionais, visualização cartográfica interativa com OpenLayers, workflows de validação técnica por analistas GIS, importação/exportação de shapefiles, integração WMS/WFS com [GEOGIS](./GEOGIS/DOCS/README.md), autenticação via [KEYCLOAK](./KEYCLOAK/README.md) SSO.

**Stack:** React 18, Vite, TypeScript, OpenLayers, Zustand, [@carf/ui](./LIB/TS/UI-COMPONENTS/DOCS/README.md), [@carf/geoapi-client](./LIB/TS/GEOAPI-CLIENT/DOCS/README.md)

### [REURBCAD](./REURBCAD/DOCS/README.md) - Mobile Field Data Collection
Aplicativo React Native para coleta de dados em campo via tablets/smartphones Android, cadastro offline-first de unidades com sincronização automática, captura de fotos georreferenciadas, assinatura digital de titulares, suporte a GPS externo Bluetooth.

**Stack:** React Native, Expo, SQLite local, [@carf/tscore](./LIB/TS/TSCORE/DOCS/README.md), React Native Maps

### [ADMIN](./ADMIN/DOCS/README.md) - Console Administrativo
Console administrativo React para super-admins e admins de tenant, gerenciamento de usuários/roles via [KEYCLOAK](./KEYCLOAK/README.md) Admin API, configuração de tenants e multi-tenancy, auditoria e logs de sistema, métricas e dashboards operacionais.

**Stack:** React 18, Next.js, TanStack Query, [@carf/ui](./LIB/TS/UI-COMPONENTS/DOCS/README.md), Keycloak Admin Client

### [GEOGIS](./GEOGIS/DOCS/README.md) - Plugin QGIS Desktop
Plugin Python para QGIS Desktop integrando camadas WMS/WFS do backend GEOAPI, edição avançada de geometrias com snapping e topologia, análises espaciais (buffer, união, interseção), exportação para formatos CAD (DWG, DXF), sincronização bidirecional com banco PostGIS.

**Stack:** Python 3.11, QGIS API, PyQt5, requests, shapely

### [KEYCLOAK](./KEYCLOAK/README.md) - Autenticação Centralizada
Keycloak customizado com temas CARF (login/account/email PT-BR), validação de CPF via [@carf/tscore](./LIB/TS/TSCORE/DOCS/README.md), realm "carf" pré-configurado com 6 clients OAuth2/OIDC, multi-tenancy dinâmico via user attributes, integração com PostgreSQL RLS através de JWT claims.

**Stack:** Keycloak 24.x, Docker, PostgreSQL, Custom Themes (Freemarker)

### [WEBDOCS](./WEBDOCS/DOCS/README.md) - Site de Documentação
Site estático VitePress com documentação técnica do sistema CARF, guias de integração para desenvolvedores, tutoriais de uso para usuários finais, API reference gerada automaticamente, hospedagem GitHub Pages ou Netlify.

**Stack:** VitePress, Vue 3, Markdown, Algolia DocSearch

## Bibliotecas TypeScript

### [@carf/tscore](./LIB/TS/TSCORE/DOCS/README.md) - Core TypeScript Library
Biblioteca compartilhada com tipos TypeScript sincronizados com backend .NET, value objects para validação (CPF, CNPJ, Email, PhoneNumber), hooks React/Vue para autenticação com [KEYCLOAK](./KEYCLOAK/README.md), utilitários de formatação e máscaras brasileiras.

**Consumidores:** [GEOWEB](./GEOWEB/DOCS/README.md), [REURBCAD](./REURBCAD/DOCS/README.md), [ADMIN](./ADMIN/DOCS/README.md), [WEBDOCS](./WEBDOCS/DOCS/README.md)

### [@carf/geoapi-client](./LIB/TS/GEOAPI-CLIENT/DOCS/README.md) - HTTP Client Library
Cliente HTTP TypeScript type-safe para GEOAPI backend, gerado automaticamente via OpenAPI/Swagger, autenticação automática com JWT Bearer tokens, interceptors para refresh token e error handling, suporte a paginação e filtros.

**Consumidores:** [GEOWEB](./GEOWEB/DOCS/README.md), [REURBCAD](./REURBCAD/DOCS/README.md), [ADMIN](./ADMIN/DOCS/README.md)

### [@carf/ui](./LIB/TS/UI-COMPONENTS/DOCS/README.md) - React Component Library
Biblioteca de componentes React reutilizáveis com shadcn/ui, componentes de domínio CARF (UnitCard, HolderCard, MapView), formulários validados com react-hook-form + zod + [@carf/tscore](./LIB/TS/TSCORE/DOCS/README.md), Storybook para desenvolvimento isolado, temas Tailwind CSS customizáveis.

**Consumidores:** [GEOWEB](./GEOWEB/DOCS/README.md), [ADMIN](./ADMIN/DOCS/README.md)

## Estrutura de Diretórios

```
PROJECTS/
├── ADMIN/              # Console administrativo Next.js
│   ├── DOCS/          # Documentação técnica
│   └── SRC-CODE/      # Código-fonte
├── GEOGIS/            # Plugin QGIS Python
│   ├── DOCS/
│   └── SRC-CODE/
├── GEOWEB/            # Portal web React
│   ├── DOCS/
│   └── SRC-CODE/
├── KEYCLOAK/          # Temas customizados Keycloak
│   ├── DOCS/
│   └── SRC-CODE/
├── REURBCAD/          # Mobile React Native
│   ├── DOCS/
│   └── SRC-CODE/
├── WEBDOCS/           # Site documentação VitePress
│   ├── DOCS/
│   └── SRC-CODE/
└── LIB/
    └── TS/
        ├── TSCORE/            # Biblioteca core TypeScript
        ├── GEOAPI-CLIENT/     # Cliente HTTP GEOAPI
        └── UI-COMPONENTS/     # Componentes React
```

## Integração entre Projetos

**Fluxo de autenticação:**
```
GEOWEB/REURBCAD/ADMIN → KEYCLOAK (OAuth2) → JWT Token → GEOAPI (validação)
```

**Fluxo de dados:**
```
REURBCAD (coleta) → GEOAPI (persistência) → PostgreSQL (RLS por tenant)
GEOWEB (visualização) ← GEOAPI (REST API) ← PostgreSQL
GEOGIS (edição) ↔ GEOAPI (WMS/WFS) ↔ PostGIS
```

**Bibliotecas compartilhadas:**
```
@carf/tscore → @carf/geoapi-client → GEOWEB/REURBCAD/ADMIN
@carf/tscore → @carf/ui → GEOWEB/ADMIN
```

## Documentação Central

Para requisitos, arquitetura e modelo de domínio compartilhados, consulte [CENTRAL](../CENTRAL/README.md).

---

**Última atualização:** 2026-01-10
