---
status: approved
updated: 2026-01-20
---

# Z-Index Scale

O sistema de z-index do ecossistema CARF gerencia camadas visuais para evitar conflitos e garantir hierarquia correta de elementos sobrepostos. O token `base` com valor 0 aplica-se ao conteudo normal no fluxo do documento. O token `dropdown` com valor 10 destina-se a dropdowns, selects, menus contextuais e autocompletes que flutuam sobre o conteudo. O token `sticky` com valor 20 serve para headers fixos e sidebars sticky que permanecem visiveis durante scroll. O token `modal` com valor 30 reserva-se para modals, dialogs, drawers e sheets que bloqueiam interacao com o conteudo abaixo. O token `popover` com valor 40 aplica-se a tooltips, popovers, hints e command palettes que podem aparecer sobre modais quando necessario. O token `toast` com valor 50 garante que notificacoes, toasts e snackbars permanecam sempre visiveis acima de qualquer outro elemento.

As CSS variables seguem nomenclatura `--z-base`, `--z-dropdown`, `--z-sticky`, `--z-modal`, `--z-popover` e `--z-toast`. Em Tailwind configuram-se as classes `z-base`, `z-dropdown`, `z-sticky`, `z-modal`, `z-popover` e `z-toast`. A regra fundamental e nunca utilizar valores arbitrarios como `z-[9999]`, sempre preferindo os tokens semanticos definidos. Backdrops de modais devem usar o mesmo z-index do elemento que cobrem. Elementos filhos herdam o contexto de empilhamento do pai, podendo-se criar contexto isolado com `isolation: isolate` quando necessario resolver conflitos. A hierarquia visual organiza-se de baixo para cima com base content em z-0, dropdown em z-10, sticky navigation em z-20, modal blocking em z-30, popover floating em z-40, e toast notifications em z-50 sempre no topo.
