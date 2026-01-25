---
type: leaf
status: approved
updated: 2026-01-24
---

# GEOWEB

Portal web React TypeScript para gestao de regularizacao fundiaria usado por analistas e gestores municipais. Interface principal para visualizar mapas interativos, cadastrar e aprovar unidades habitacionais, vincular titulares, gerenciar processos de legitimacao e gerar relatorios.

Stack frontend moderna com React 18, TypeScript, Vite, TanStack Query para data fetching, Zustand para estado global, shadcn/ui para componentes e react-leaflet para mapas. Autenticacao OAuth2 PKCE via Keycloak com protected routes e tenant switcher para usuarios com acesso a multiplos municipios.

## Capacidades

Mapas interativos com camadas WMS/WMTS configuraveis por tenant. Formularios de cadastro com validacao client-side usando React Hook Form e Zod. Dashboard com metricas de progresso por comunidade. Fluxo de aprovacao com historico de alteracoes. Exportacao de dados geograficos. Detalhes tecnicos no repositorio carf-geoweb.
