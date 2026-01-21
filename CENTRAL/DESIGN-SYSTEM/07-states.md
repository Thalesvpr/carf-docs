---
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata. Stub de 13 linhas - incompleto."
updated: 2026-01-20
---

# Interactive States

O sistema de estados interativos do ecossistema CARF especifica feedback visual consistente para todos os componentes. O estado focus para navegacao por teclado utiliza ring width de 2px na cor azul `#3872C6` com ring offset de 2px, substituindo outline padrao por box-shadow com `0 0 0 2px white, 0 0 0 4px var(--color-blue)` aplicado via pseudo-classe `:focus-visible`. O estado disabled para elementos inativos aplica opacity 0.5, cursor `not-allowed` e pointer-events `none`, desabilitando completamente efeitos de hover e focus, com suporte tanto para atributo `disabled` quanto `aria-disabled="true"`.

O estado hover fornece feedback ao passar o mouse, onde buttons primary escurecem background em 10%, buttons secondary ganham background sutil, links recebem underline com cor escurecida, cards aumentam elevacao via shadow, e rows ou items ganham background sutil. O estado active ou pressed ao clicar aplica `transform: scale(0.98)` com background escurecido em 15% e transicao de 100ms. O estado error para validacao falha utiliza border-color e text-color no vermelho accent `#E63946`, icone de exclamacao circular e background `rgba(230,57,70,0.05)` para destaque sutil, aplicado via atributo `aria-invalid="true"` ou classe `.error`. O estado loading indica carregamento com opacity 0.7 no conteudo, cursor `wait` e spinner animado.

As CSS variables incluem `--ring-width`, `--ring-color`, `--ring-offset` para focus, `--disabled-opacity` para disabled, `--error-color` e `--error-bg` para erro, `--hover-opacity` e `--hover-bg-subtle` para hover. Em Tailwind utilizam-se classes como `focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2` para focus, `disabled:opacity-50 disabled:cursor-not-allowed` para disabled, `hover:shadow-md transition-shadow` para hover em cards, e `active:scale-[0.98]` para pressed. A acessibilidade exige focus sempre visivel para navegacao por teclado, contraste minimo WCAG AA em todos os estados, indicadores multiplos que nao dependam apenas de cor combinando cor com icone e texto, e uso correto de atributos ARIA como `aria-disabled` e `aria-invalid`.
