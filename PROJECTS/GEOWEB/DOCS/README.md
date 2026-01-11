# GEOWEB - Portal Web de Gestão REURB

**[📋 Overview de Implementação](./OVERVIEW.md)** - Mapeamento completo de requirements, domain model e arquitetura técnica

Portal web React + Vite para gestão de processos de regularização fundiária urbana (REURB) permitindo técnicos municipais e gestores visualizarem mapas de comunidades, cadastrarem unidades habitacionais online, gerenciarem titulares, acompanharem processos de legitimação, e exportarem relatórios, integrando com backend [GEOAPI](../../GEOAPI/DOCS/ARCHITECTURE/01-overview.md) via [@carf/geoapi-client](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md) consumindo APIs REST documentadas em [CENTRAL/API](../../../CENTRAL/API/README.md), autenticação via [Keycloak](../../KEYCLOAK/DOCS/README.md) conforme [ADR-003](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md), UI com componentes [@carf/ui](../../LIB/TS/UI-COMPONENTS/DOCS/README.md) baseados em [shadcn/ui](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-014-shadcn-ui-component-library.md), mapas interativos com layers WMS visualizando comunidades e unidades georreferenciadas conforme [UC-010](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md), server state via [TanStack Query](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-015-tanstack-query-server-state.md), client state via [Zustand](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-019-zustand-client-state.md), build via [Vite](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-012-vite-bundler-frontend.md), e deployment em [Vercel](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-013-vercel-deployment-platform.md) com preview deployments automáticos.

## Funcionalidades Principais

**Gestão de Unidades** - CRUD completo de unidades habitacionais com formulários validados client-side via [@carf/tscore](../../LIB/TS/TSCORE/DOCS/CONCEPTS/01-value-objects.md), upload de fotos, desenho de polígonos no mapa, e sincronização com backend [GEOAPI /api/units](../../../CENTRAL/API/UNITS/README.md).

**Visualização de Mapas** - Mapas interativos com react-leaflet ou MapLibre renderizando layers WMS de comunidades, unidades individuais como markers, sobreposição de ortofotos e limites municipais, ferramentas de medição de área/distância, e export para formatos GIS conforme [UC-007](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md).

**Gestão de Titulares** - Cadastro de posseiros vinculados a unidades com validação CPF/CNPJ, documentos anexados, e histórico de alterações consumindo [GEOAPI /api/holders](../../../CENTRAL/API/HOLDERS/README.md).

**Processos de Legitimação** - Visualização de workflow de aprovação com status transitions, upload de documentação obrigatória conforme Lei 13.465/2017, comentários de técnicos/fiscais, e aprovação/rejeição via [GEOAPI /api/legitimation](../../../CENTRAL/API/LEGITIMATION/README.md).

**Relatórios e Exportações** - Geração assíncrona de relatórios PDF/Excel por comunidade ou município completo, exportação de shapefiles para QGIS, e dashboards com estatísticas demographics via [GEOAPI /api/reports](../../../CENTRAL/API/REPORTS/README.md).

Ver [índice completo de features implementadas](./FEATURES/README.md) mapeando casos de uso do sistema.

## Documentação

- **[Arquitetura](./ARCHITECTURE/README.md)** - Decisões técnicas de integração Keycloak e @carf/tscore
- **[Conceitos](./CONCEPTS/README.md)** - Autenticação, protected routes, tenant switcher
- **[Guias Práticos](./HOW-TO/README.md)** - Setup Keycloak, login/logout, refresh tokens
- **[Camadas](./LAYERS/README.md)** - Estrutura de código React (AuthContext, API layer, UI components)

## Stack Tecnológico

- **Framework:** React 18 + TypeScript 5 + Vite 5 conforme [ADR-012](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-012-vite-bundler-frontend.md)
- **Routing:** React Router 6 com protected routes
- **Server State:** TanStack Query v5 conforme [ADR-015](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-015-tanstack-query-server-state.md)
- **Client State:** Zustand conforme [ADR-019](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-019-zustand-client-state.md)
- **UI Library:** shadcn/ui + Radix conforme [ADR-014](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-014-shadcn-ui-component-library.md)
- **Maps:** react-leaflet ou MapLibre GL JS
- **Forms:** React Hook Form + Zod validation
- **API Client:** [@carf/geoapi-client](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md)
- **Deployment:** Vercel conforme [ADR-013](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-013-vercel-deployment-platform.md)

## Código Fonte

Ver [carf-geoweb README](../SRC-CODE/carf-geoweb/README.md) para instruções de build, instalação e desenvolvimento local.

---

**Última atualização:** 2025-01-10
