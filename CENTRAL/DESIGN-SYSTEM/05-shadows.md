---
status: approved
updated: 2026-01-20
---

# Shadows

O sistema de sombras do ecossistema CARF estabelece uma escala de elevacao visual para criar hierarquia de interface e indicar profundidade dos elementos. O token `none` remove qualquer sombra para elementos flat e inline. O token `sm` com valor `0 1px 2px rgba(0,0,0,0.05)` aplica-se a inputs e buttons em estado de repouso, criando elevacao sutil de nivel 0.5. O token `DEFAULT` com `0 4px 6px rgba(0,0,0,0.1)` destina-se a cards e containers no nivel 1 de elevacao. O token `md` com `0 6px 12px rgba(0,0,0,0.15)` serve para dropdowns, menus flutuantes e tooltips no nivel 2. O token `lg` com `0 10px 25px rgba(0,0,0,0.2)` reserva-se para modals, dialogs e toasts no nivel 3. O token `xl` com `0 20px 40px rgba(0,0,0,0.25)` aplica-se a overlays criticos como command palettes no nivel 4.

As CSS variables seguem o padrao `--shadow-none`, `--shadow-sm`, `--shadow` para o valor padrao, `--shadow-md`, `--shadow-lg` e `--shadow-xl`. Em Tailwind usam-se classes `shadow-none`, `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg` e `shadow-xl`. A hierarquia de aplicacao determina que elementos base nao tenham sombra ou usem `sm`, containers utilizem `DEFAULT`, elementos flutuantes apliquem `md`, e overlays modais empreguem `lg` ou `xl`. Transicoes de sombra devem animar suavemente em 200ms para feedback visual fluido. Em modo escuro, sombras tornam-se menos visiveis naturalmente, recomendando-se valores de opacidade aumentados como `rgba(0,0,0,0.3)` para `DEFAULT`, `rgba(0,0,0,0.4)` para `md` e `rgba(0,0,0,0.5)` para `lg`, alem de bordas sutis como complemento visual.
