---
type: adr
status: approved
updated: 2026-02-07
---

# ADR-002: Zustand para Gerenciamento de Estado

## Contexto

O REURBCAD precisa de gerenciamento de estado global para coordenar informacoes entre telas que nao compartilham hierarquia de componentes: token de autenticacao acessado em toda requisicao, status de sincronizacao visivel em multiplas telas, estado do mapa compartilhado entre componentes de navegacao e formulario, e rascunho do formulario preservado durante navegacao entre telas do wizard de cadastro. A escolha precisa equilibrar simplicidade com capacidade suficiente para esses cenarios sem introduzir boilerplate excessivo em um app mobile onde cada kilobyte de bundle importa.

## Decisao

Zustand como biblioteca unica de gerenciamento de estado global. Quatro stores isoladas por dominio, cada uma independente e importavel apenas onde necessaria.

A useAuthStore armazena o token JWT atual, dados do usuario autenticado (id, nome, email, role), o tenant ativo (id e nome do municipio) e flags de estado como isAuthenticated e isTokenExpired. Essa store e hidratada no boot do app a partir do SecureStore do Expo e atualizada a cada refresh de token. Todas as chamadas HTTP leem o token dessa store via interceptor do cliente HTTP.

A useSyncStore rastreia o estado da sincronizacao: status atual (idle, pulling, pushing, error), timestamp da ultima sync bem-sucedida, contagem de operacoes pendentes na fila, lista de conflitos aguardando resolucao manual e progresso percentual durante operacoes de sync. Componentes em qualquer tela podem exibir indicador de sync lendo essa store.

A useMapStore mantem a regiao visivel do mapa (latitude, longitude, deltas de latitude e longitude), array de IDs de layers visiveis, nivel de zoom atual e coordenadas do usuario obtidas via GPS. Compartilhada entre o componente de mapa, os controles de layer e a logica de selecao de poligono.

A useFormStore preserva o rascunho do formulario de cadastro durante navegacao entre steps do wizard: dados da unidade parcialmente preenchidos, dados do titular em edicao, step atual do wizard (1 a 4), array de IDs de fotos ja capturadas e flag indicando se o formulario tem alteracoes nao salvas. Quando o usuario finaliza o cadastro, a store e limpa. Se o app for fechado antes da finalizacao, o rascunho persiste via middleware zustand/persist com AsyncStorage.

## Justificativa

Zustand tem bundle de 1.1KB gzipped, sem boilerplate de reducers ou actions, sem provider wrapper na arvore de componentes, e API baseada em hooks que integra naturalmente com React Native. Stores isoladas por dominio evitam re-renders desnecessarios pois cada componente subscreve apenas aos campos que usa via selectors. O middleware zustand/persist permite hidratacao automatica de stores criticas (auth e form) a partir de AsyncStorage sem codigo adicional.

## Alternativas Descartadas

Redux Toolkit descartado por boilerplate excessivo (slices, reducers, actions, selectors) desproporcional para um app mobile com quatro stores simples, alem de bundle 5x maior. Context API descartado por causar re-renders em cascata em toda a arvore ao atualizar qualquer valor do contexto, problema critico em telas com mapa que precisam de 60fps. MobX descartado por uso de decorators e observables que adicionam complexidade conceitual sem beneficio proporcional para o tamanho do estado gerenciado.
