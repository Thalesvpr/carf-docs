# PROJECTS

Implementações técnicas do sistema CARF organizadas em sete projetos principais (GEOAPI backend REST API .NET 9 + PostgreSQL + PostGIS implementando Clean Architecture DDD CQRS, GEOWEB portal web React 18 + Vite gestão geoespacial unidades habitacionais mapas interativos, REURBCAD mobile React Native + Expo offline-first coleta campo GPS fotos sincronização, GEOGIS plugin QGIS Python análises espaciais WMS/WFS integração PostGIS, ADMIN console React SPA gestão usuários tenants via Keycloak Admin API, KEYCLOAK autenticação OAuth2/OIDC SSO multi-tenancy temas customizados PT-BR, WEBDOCS portal VitePress Vue 3 documentação técnica interativa) e três bibliotecas TypeScript compartilhadas (@carf/tscore value objects CPF CNPJ validações hooks React/Vue autenticação, @carf/geoapi-client HTTP client type-safe OpenAPI gerado automaticamente, @carf/ui componentes React shadcn/ui formulários domínio CARF) seguindo decisões arquiteturais documentadas em CENTRAL/ARCHITECTURE implementando domain model unificado com rastreabilidade bidirecional entre requisitos funcionais em CENTRAL/REQUIREMENTS e features implementadas em cada PROJECTS/[PROJETO]/DOCS/FEATURES estabelecendo navegação conceitual entre especificação produto e código técnico. Cada projeto mantém repositório Git independente em PROJECTS/[PROJETO]/SRC-CODE/carf-[projeto] com documentação específica técnica em PROJECTS/[PROJETO]/DOCS contendo arquitetura decisões Keycloak integration, conceitos autenticação state management offline-first, guias práticos setup build deploy troubleshooting, e estrutura código por camadas Domain Application Infrastructure Presentation.

## Projetos

- **[GEOAPI](./GEOAPI/DOCS/README.md)** - Backend REST API .NET 9
- **[GEOWEB](./GEOWEB/DOCS/README.md)** - Portal web React 18
- **[REURBCAD](./REURBCAD/DOCS/README.md)** - Mobile app React Native
- **[GEOGIS](./GEOGIS/DOCS/README.md)** - Plugin QGIS Python
- **[ADMIN](./ADMIN/DOCS/README.md)** - Console admin React SPA
- **[KEYCLOAK](./KEYCLOAK/DOCS/README.md)** - Autenticação OAuth2/OIDC
- **[WEBDOCS](./WEBDOCS/DOCS/README.md)** - Portal documentação VitePress

## Bibliotecas

- **[@carf/tscore](./LIB/TS/TSCORE/DOCS/README.md)** - Biblioteca TypeScript core
- **[@carf/geoapi-client](./LIB/TS/GEOAPI-CLIENT/DOCS/README.md)** - HTTP client GEOAPI
- **[@carf/ui](./LIB/TS/UI-COMPONENTS/DOCS/README.md)** - Componentes React UI

---

**Última atualização:** 2026-01-11
