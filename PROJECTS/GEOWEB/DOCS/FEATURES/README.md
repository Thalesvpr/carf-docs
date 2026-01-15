# GEOWEB - Features

Portal web SPA React TypeScript implementando interface completa gestão regularização fundiária urbana para usuários autorizados ADMIN MANAGER ANALYST visualizarem cadastrarem aprovarem unidades habitacionais titulares processos legitimação geração relatórios exportação dados geoespaciais através de arquitetura moderna client-side rendering Vite build tool React 18 concurrent features TanStack Query server state management Zustand client state React Hook Form Zod validations React Router DOM navegação React Leaflet visualização mapas interativos integration GEOAPI backend REST API autenticação Keycloak OAuth2 PKCE multi-tenancy RLS garantindo isolamento dados municipais.

## Features Implementadas

- **[unit-management.md](./01-unit-management.md)** - CRUD unidades habitacionais wizard multi-step validações Zod aprovação workflow status transitions TanStack Table pagination filtering React Leaflet map visualization
- **[holder-management.md](./02-holder-management.md)** - CRUD titulares pessoas físicas validação CPF vinculação unidades many-to-many relationship upload documentos React Dropzone compression storage blob
- **[gis-integration.md](./04-gis-integration.md)** - Integração SIG React Leaflet visualização mapas interativos layers Units Communities WMS WMTS drawing tools polygon capture spatial queries PostGIS ST_Intersects validation
- **[legitimation-process.md](./06-legitimation-process.md)** - Workflow management processos legitimação REURB-S REURB-E checklist tasks timeline tracking documents approval permissions MANAGER ADMIN state machine transitions
- **[reporting.md](./07-reporting.md)** - Geração relatórios dashboard metrics charts Recharts aggregated data exportação PDF CSV Excel async processing job tracking download
- **[shapefile-import.md](./05-shapefile-import.md)** - Importação bulk shapefiles wizard upload validation attribute mapping topology checking CRS compatibility preview map async processing NetTopologySuite
- **[team-management.md](./03-team-management.md)** - CRUD equipes técnicas assignment members communities roles COORDINATOR ANALYST FIELD_AGENT notifications email push audit logging

Funcionalidades principais incluem Unit Management CRUD completo unidades habitacionais com formulários multi-step validações inline persistência GEOAPI aprovação workflow status transitions pending approved rejected comments justification tracking auditoria, Holder Management CRUD titulares pessoas físicas validações CPF RG vinculação múltiplas unidades relacionamento one-to-many many-to-many upload documentos photos storage blob, GIS Integration visualização mapas React Leaflet com layers Units Communities boundaries base maps OpenStreetMap satellite imagery overlay WMS WMTS external sources IBGE MapBiomas drawing tools polygon capture editing spatial queries intersection containment buffer analysis, Reporting geração relatórios comunidade units dashboard aggregated metrics occupancy status approval rates export PDF Excel CSV formats charts visualization via Recharts pie bar line graphs, Team Management CRUD equipes técnicas atribuição membros roles comunidades coordenação trabalho campo visualização assignments filtering, Legitimation Process workflow management status tracking documentation requirements checklist validation approval signatures digital timestamps legal compliance REURB-S REURB-E distinct flows, Shapefile Import upload validation attribute mapping preview geometries bulk insert error handling duplicate detection conflict resolution progress tracking.

Stack tecnológica React 18.3 TypeScript 5.3 strict mode Vite 5.0 build bundler TanStack Query v5 server state com cache invalidation optimistic updates retry logic persistence localStorage, Zustand lightweight state management stores UI ephemeral selected filters modals sidebar expansion, React Router DOM v6 nested routes lazy loading code splitting protected routes role-based guards, React Hook Form v7 useForm hook controlled components Zod v3 schema validation resolver integration onChange validation inline errors, React Leaflet v4 Leaflet.js wrapper MapContainer TileLayer Marker Polygon drawing via leaflet-draw plugin geospatial visualization, Axios HTTP client interceptors request response authentication retry exponential backoff error handling, React Query DevTools debugging cache inspection mutations tracking, Recharts declarative charts components ResponsiveContainer LineChart BarChart PieChart data visualization dashboards.

Arquitetura SPA client-side routing React Router DOM routes nested layouts protected via PrivateRoute component checking authentication roles via useAuth hook redirecting login forbidden conforme permissions, state management híbrido TanStack Query para server state cached staleTime refetchOnWindowFocus automatic background refetching Zustand para UI state ephemeral modals filters selections não persistidos, forms React Hook Form useForm register handleSubmit errors validation Zod schemas type-safe runtime validation custom validators async uniqueness checks debounced, API integration custom hooks useUnits useCreateUnit useUpdateUnit useDeleteUnit encapsulating TanStack Query useQuery useMutation with keys dependencies enabled conditions retry logic onSuccess onError callbacks cache invalidation queryClient.invalidateQueries targeted specific keys, authentication AuthContext provider wrapping App tree useAuth hook exposing user isAuthenticated login logout switchTenant hasRole getToken methods consuming keycloak-js library OAuth2 flows token refresh interceptors, routing file-based structure src/pages directory UnitsListPage UnitDetailsPage UnitFormPage protected requiring authentication role permissions layouts DashboardLayout AuthLayout wrapping pages headers sidebars footers, components atomic design atoms Button Input Select molecules FormField Card organisms UnitCard UnitTable templates PageTemplate compositions reusable composable typed props.

Relacionamento requirements implementando UC-001 cadastro unidades UC-002 aprovação UC-003 vinculação titulares UC-006 relatórios UC-007 exportação UC-008 importação shapefiles UC-009 legitimação UC-010 camadas GIS UC-011 gestão equipes garantindo usuários web ADMIN MANAGER ANALYST produtivos interface intuitiva responsiva acessível workflows eficientes aprovação validação coordenação campo reporting accountability compliance LGPD multi-tenancy RLS.

---

**Última atualização:** 2026-01-11

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (7 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-unit-management](./01-unit-management.md) | Unit Management - Gestão de Unidades |
| [02-holder-management](./02-holder-management.md) | Holder Management - Gestão de Titulares |
| [03-team-management](./03-team-management.md) | Team Management - Gestão de Equipes |
| [04-gis-integration](./04-gis-integration.md) | GIS Integration - Integração SIG |
| [05-shapefile-import](./05-shapefile-import.md) | Shapefile Import - Importação |
| [06-legitimation-process](./06-legitimation-process.md) | Legitimation Process - Processo de Legitimação |
| [07-reporting](./07-reporting.md) | Reporting - Relatórios |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (7) antes do rodapé - considerar converter para parágrafo denso.
