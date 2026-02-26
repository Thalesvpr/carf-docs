---
type: leaf
status: review
updated: 2026-02-07
---

# Layers - ADMIN

## Camadas

REURBMASTER SPA possui cinco camadas organizadas hierarquicamente. A Presentation Layer contem React components em src/pages/ e src/components/ renderizando UI com shadcn/ui. A State Management Layer utiliza TanStack Query para gerenciar server state incluindo cache, refetch e mutations, enquanto Zustand gerencia client state como UI flags, modals e selected items. A API Client Layer implementa @carf/geoapi-client para fazer requests HTTP aos endpoints /api/admin/ do GEOAPI com JWT injection automatico via interceptor. A Routing Layer usa React Router v6 com protected routes que validam role antes de renderizar paginas admin. Por fim, a Auth Layer utiliza @carf/tscore KeycloakClient gerenciando login, logout e token refresh com PKCE flow sem client_secret no frontend.

## Organizacao das Camadas

| Camada | Responsabilidade | Tecnologia |
|--------|-----------------|------------|
| Presentation | Renderizar UI e componentes visuais | React, shadcn/ui |
| State Management | Cache de server state e client state | TanStack Query, Zustand |
| API Client | Requests HTTP com auth automatico | @carf/geoapi-client, interceptors |
| Routing | Navegacao e protecao de rotas | React Router v6, protected routes |
| Auth | Login, logout, refresh de tokens | @carf/tscore KeycloakClient, PKCE |

O fluxo de dados percorre as camadas de cima para baixo: a Presentation Layer dispara acoes que passam pela State Management Layer, que invoca a API Client Layer, enquanto Routing e Auth atuam transversalmente validando permissoes e injetando credenciais em cada requisicao.
