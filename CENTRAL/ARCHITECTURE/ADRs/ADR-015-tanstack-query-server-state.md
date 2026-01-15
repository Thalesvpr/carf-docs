# ADR-015: Escolha do TanStack Query para Server State Management

Decisão arquitetural escolhendo TanStack Query (React Query) como solução de server state management para frontends React (GEOWEB ADMIN) justificada por cache automático inteligente deduplicando requests idênticos simultâneos economizando bandwidth e reduzindo carga no backend GEOAPI, background refetching mantendo dados atualizados transparentemente sem bloquear UI melhorando perceived performance, stale-while-revalidate strategy servindo cache imediatamente enquanto revalida em background proporcionando instant feedback, invalidação precisa de cache via query keys permitindo invalidar apenas dados modificados após mutations mantendo resto do cache válido, retry automático com exponential backoff em falhas de rede resiliente a conectividade instável comum em áreas rurais, optimistic updates permitindo UI instantaneamente responsiva antes de confirmação do servidor melhorando UX, pagination e infinite scroll built-in simplificando implementação de listas grandes de unidades/holders, devtools integrado facilitando debugging de cache queries estado de loading durante desenvolvimento, e SSR/SSG ready preparando eventual migration para Next.js mantendo mesma API.

TanStack Query v5 especificamente adiciona typed API melhorada com TypeScript inference automático, simplified mutation API reduzindo boilerplate, e improved garbage collection liberando memória de queries unused.

Alternativas consideradas incluem SWR (rejeitado por features limitadas comparado a React Query faltando optimistic updates e invalidação granular), Apollo Client (rejeitado por ser GraphQL-specific enquanto GEOAPI usa REST), RTK Query (rejeitado por coupling com Redux toolkit exigindo Redux store mesmo para apps simples), fetch manual com useState (rejeitado por reinventar wheel de cache retry loading states), e Zustand para server state (rejeitado por não ser propósito-específico para server state).

Consequências positivas incluem developer experience excepcional com boilerplate mínimo, performance superior com cache inteligente, UX melhorada com optimistic updates, bandwidth economizado com deduplication, e código declarativo fácil de testar. Consequências negativas incluem bundle size de ~35KB gzipped adicionando overhead, curva de aprendizado de conceitos de caching, e debugging ocasionalmente complexo quando cache comporta-se inesperadamente.

Configuração específica usa QueryClient com staleTime: 30000 (30s), cacheTime: 300000 (5min), retry: 3 com exponential backoff, refetchOnWindowFocus: false evitando refetch excessivo, e QueryClientProvider wrapping app.

Status da decisão é aprovado e implementado desde 2024-Q3.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + Frontend
**Última revisão:** 2025-01-10
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
