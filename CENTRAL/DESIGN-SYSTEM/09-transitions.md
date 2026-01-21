---
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata."
updated: 2026-01-20
---

# Transitions

O sistema de transicoes do ecossistema CARF especifica animacoes para feedback visual fluido e consistente. A escala de duracao define `fast` com 150ms para hover, focus e micro-interacoes, `DEFAULT` com 200ms para a maioria das transicoes, `slow` com 300ms para modais, acordeoes e expansoes, e `slower` com 500ms para animacoes de entrada de pagina. A escala de easing define `DEFAULT` com `cubic-bezier(0.4, 0, 0.2, 1)` para movimento natural, `in` com `cubic-bezier(0.4, 0, 1, 1)` para aceleracao de entrada, `out` com `cubic-bezier(0, 0, 0.2, 1)` para desaceleracao de saida, e `in-out` para combinacao de ambos.

As propriedades animaveis seguem configuracoes especificas onde opacity, background-color, border-color e color utilizam duracao fast com easing out, transform e box-shadow utilizam duracao DEFAULT, e height ou width utilizam duracao slow. Por componente, buttons animam colors e transform em fast, inputs animam border-color e shadow em fast, cards animam shadow em DEFAULT, modals e dropdowns animam opacity e transform em DEFAULT, accordions animam height em slow, e tooltips animam opacity em fast. As CSS variables incluem `--duration-fast`, `--duration-default`, `--duration-slow`, `--duration-slower` para duracoes e `--ease-default`, `--ease-in`, `--ease-out`, `--ease-in-out` para easings. Os keyframes comuns incluem fadeIn para opacity de 0 a 1, slideUp para translateY de 10px a 0 com fade, scaleIn para scale de 0.95 a 1 com fade, e accordionDown para height de 0 ao valor final.

A acessibilidade exige respeitar preferencias do usuario via media query `prefers-reduced-motion: reduce`, reduzindo duration para 0.01ms ou desabilitando animacoes completamente. Em Tailwind utilizam-se classes `motion-safe:transition-all` e `motion-reduce:transition-none`. As regras fundamentais sao usar tokens em vez de valores arbitrarios, preferir transform e opacity por serem GPU accelerated com melhor performance, garantir que animacoes tenham proposito funcional e nao apenas decorativo, e aplicar duracoes rapidas para feedback imediato e lentas para direcionar atencao do usuario.
