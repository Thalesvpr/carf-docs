---
type: leaf
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata. Stub de 11 linhas - incompleto."
updated: 2026-01-20
---

# Breakpoints

O sistema de breakpoints do ecossistema CARF segue a estrategia mobile-first para garantir experiencia consistente em todos os dispositivos. O token `sm` em 640px destina-se a smartphones em orientacao paisagem. O token `md` em 768px aplica-se a tablets em orientacao retrato. O token `lg` em 1024px serve para laptops e desktops padrao. O token `xl` em 1280px atende monitores grandes e wide. O token `2xl` em 1536px reserva-se para monitores ultrawide. Os container widths correspondentes sao 100% para mobile base, 640px em `sm`, 768px em `md`, 1024px em `lg`, 1280px em `xl` e 1400px em `2xl`.

As CSS variables utilizam nomenclatura `--breakpoint-sm`, `--breakpoint-md`, `--breakpoint-lg`, `--breakpoint-xl` e `--breakpoint-2xl`. Media queries seguem abordagem mobile-first com `min-width` progressivo. Em Tailwind, a configuracao de screens define os mesmos valores, enquanto container configura-se centralizado com padding responsivo de 1rem no base, 2rem em `sm`, 4rem em `lg`, 5rem em `xl` e 6rem em `2xl`. O layout mobile base abaixo de 640px utiliza navegacao em bottom bar ou hamburger menu com conteudo em coluna unica e cards empilhados verticalmente. O layout tablet em `md` introduz grid de 2 colunas com sidebar colapsavel e navegacao em top bar. O layout desktop em `lg` apresenta sidebar fixa, grid multi-coluna e todas as features visiveis. O layout wide em `xl` e `2xl` centraliza conteudo com max-width, aumenta espacamento entre elementos e opcionalmente amplia tipografia para melhor aproveitamento do espaco disponivel.
