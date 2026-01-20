---
status: review
updated: 2026-01-17
---

# Diagramas Mermaid

Mermaid permite criar diagramas a partir de sintaxe textual em arquivos Markdown renderizados como SVG no build time sem JavaScript client-side. Suporta flowcharts, sequence diagrams, class diagrams, ER diagrams, gantt charts, e outros tipos.

Sintaxe em code blocks com linguagem mermaid é processada pelo plugin @astrojs/mermaid durante build. Texto é convertido para SVG inline no HTML resultante. Diagramas são indexados pelo Pagefind permitindo busca por texto dentro de diagramas.

Flowchart documenta fluxos de processo com nós e setas direcionais. Sintaxe graph TD para top-down ou graph LR para left-right define direção. Nós são definidos com id e label entre colchetes ou parênteses para diferentes formas. Setas com texto descrevem transições.

Sequence diagram documenta interações entre componentes ao longo do tempo. Sintaxe sequenceDiagram seguido de participantes e mensagens com setas. Útil para documentar fluxos de autenticação, chamadas de API, e comunicação entre serviços.

ER diagram documenta modelo de dados com entidades e relacionamentos. Sintaxe erDiagram com entidades contendo atributos e relacionamentos entre elas usando notação de cardinalidade. Útil para documentar schema do banco de dados.

Temas do Mermaid configurados em astro.config.mjs aplicam cores do design system CARF aos diagramas. Tema escuro ativado automaticamente quando usuário usa dark mode do site mantendo legibilidade em ambos modos.
