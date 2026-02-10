---
type: leaf
status: review
updated: 2026-02-08
---

# Frontend Patterns

Os padroes frontend do ecossistema CARF padronizam implementacao entre GEOWEB (React SPA), ADMIN (React Vite SPA) e REURBCAD (React Native Expo), compartilhando logica via bibliotecas @carf/tscore e @carf/ui.

## State Management

O gerenciamento de estado segue separacao entre server state e client state. Server state (dados da API) e gerenciado via TanStack Query com cache automatico, invalidacao por mutation, optimistic updates para cadastro de unidades e retry automatico em falhas de rede. Client state (UI, formularios) e gerenciado via Zustand para estados globais simples como tema e sidebar, e React Hook Form para estado de formularios com validacao Zod.

## Componentes e Formularios

Componentes seguem padrao function components com hooks, compound components para UI complexas (FormField com Label, Input e Error) e composicao via children. Formularios utilizam React Hook Form integrando validacoes do @carf/tscore/validations (CPF Mod-11, CNPJ, Email, Phone) via resolvers Zod, garantindo regras de negocio brasileiras consistentes entre projetos. Field-level errors sao exibidos inline abaixo de cada campo.

## Autenticacao e Rotas

O AuthProvider do @carf/tscore/auth/react gerencia sessao OAuth2 com Keycloak, fornecendo isAuthenticated, user, roles e funcoes login/logout via context. ProtectedRoute verifica autenticacao e requiredRoles antes de renderizar, redirecionando para login quando necessario. Rotas usam React Router v6 no GEOWEB e file-based routing no ADMIN, com lazy loading para code-splitting.

## Mapas

GEOWEB utiliza React Leaflet para renderizacao de mapas interativos com poligonos de unidades coloridos por status, clustering em zoom baixo via react-leaflet-cluster, popup com informacoes resumidas ao clicar e suporte a tiles XYZ de ortofotos. REURBCAD utiliza react-native-maps com MapView integrada a GPS nativo para captura de coordenadas em campo.

## Type Safety

Interfaces TypeScript de entidades de dominio (Unit, Holder, Community) sao compartilhadas via @carf/tscore/types, sincronizadas com o backend .NET para garantir contratos API type-safe em compile-time.
