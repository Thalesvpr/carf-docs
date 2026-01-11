# ADR-019: Escolha do Zustand para Client State Management

Decisão arquitetural escolhendo Zustand como solução de client state management para frontends React (GEOWEB ADMIN) justificada por simplicidade extrema com API minimalista baseada em hooks evitando boilerplate verboso de Redux/Context, bundle size mínimo de ~1KB gzipped versus ~12KB Redux RTK, performance superior sem re-renders desnecessários através de subscriptions granulares permitindo components subscriberem apenas slices específicos de state, DevTools integration para debugging time-travel, persistence middleware para sync com localStorage, absence de Provider wrapping mantendo código limpo, TypeScript inference automático sem definições manuais de types, e middleware ecosystem permitindo logging immer devtools persist.

Zustand especificamente adequado para UI state (sidebar aberto modal ativo selected items filter values) versus server state gerenciado por TanStack Query, evitando confusion de responsabilidades mantendo concerns separados.

Alternativas consideradas incluem Redux Toolkit (rejeitado por verbosidade e overhead desnecessário para client state simples), Context API (rejeitado por re-render issues e ausência de DevTools), Jotai (rejeitado por atomic approach inadequado para state estruturado), Recoil (rejeitado por Meta-specific e declínio de adoção), Valtio (rejeitado por proxy-based approach com overhead de performance), e useState props drilling (rejeitado por não escalar e dificultar manutenção).

Consequências positivas incluem developer experience excepcional, bundle size mínimo, performance superior, código declarativo testável, e migração gradual possível. Consequências negativas incluem ausência de time-travel debugging nativo (apenas via middleware), ecosistema menor que Redux, e risco de overuse para server state (mitigado com guidelines claras separando concerns).

Configuração utiliza Zustand 4.x com store separadas por domínio (uiStore authStore filtersStore), DevTools habilitado em development, persist middleware para sidebar preferences, e custom middleware para logging actions em development.

Status aprovado e implementado desde 2024-Q3.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + Frontend
**Última revisão:** 2025-01-10
