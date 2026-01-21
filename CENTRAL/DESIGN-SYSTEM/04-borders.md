---
status: review
updated: 2026-01-20
---

# Borders

O sistema de border-radius do ecossistema CARF define seis tokens padronizados para consistencia visual em todos os componentes. O token `none` com valor 0 aplica-se a elementos quadrados sem arredondamento. O token `sm` com 4px destina-se a inputs, badges, chips e tooltips que requerem bordas sutis. O token `DEFAULT` com 8px e o padrao para botoes, cards, containers e alerts, sendo o mais utilizado no sistema. O token `md` com 12px aplica-se a modals, dialogs, dropdowns e menus que necessitam maior destaque visual. O token `lg` com 16px reserva-se para cards destacados e panels de maior importancia hierarquica. O token `full` com 9999px cria formas completamente circulares para avatares, pills, tags e toggles.

As CSS variables correspondentes seguem a nomenclatura `--radius-none`, `--radius-sm`, `--radius` para o valor padrao, `--radius-md`, `--radius-lg` e `--radius-full`. Em Tailwind utilizam-se as classes utilitarias `rounded-none`, `rounded-sm`, `rounded` para o padrao, `rounded-md`, `rounded-lg` e `rounded-full`. A regra fundamental e nunca utilizar valores arbitrarios, sempre preferindo os tokens definidos. A hierarquia visual exige que elementos menores utilizem raios menores, enquanto containers maiores podem usar raios mais expressivos. No aninhamento de componentes, o container externo deve sempre ter border-radius igual ou maior que seus elementos filhos internos. Bordas arredondadas tambem contribuem para acessibilidade ao facilitar o reconhecimento visual de areas clicaveis e interativas.
