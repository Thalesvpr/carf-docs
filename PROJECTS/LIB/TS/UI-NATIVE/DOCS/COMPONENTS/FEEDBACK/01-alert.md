---
type: leaf
status: review
updated: 2026-01-24
---

# Alert

Componente de alerta inline com icone e variantes de severidade.

## Props

Prop variant aceita default, destructive, warning ou success definindo cor e icone. Prop title exibe texto principal em negrito. Prop description exibe texto secundario com detalhes. Prop icon aceita componente customizado substituindo icone padrao.

## Variantes

Variante default usa borda e fundo neutros para informacoes gerais. Variante destructive usa vermelho para erros e falhas. Variante warning usa amarelo para avisos importantes. Variante success usa verde para confirmacoes positivas.

## Icones

Cada variante inclui icone padrao apropriado. Info circle para default, exclamation para destructive, warning triangle para warning e check circle para success. Prop icon substitui icone padrao por customizado.

## Acessibilidade

AccessibilityRole definido como alert para anuncio imediato. Variante destructive usa accessibilityLiveRegion assertive. Icone decorativo usa accessibilityElementsHidden true. Texto completo anunciado em sequencia.

## Layout

Container usa flexbox com icone a esquerda e textos empilhados. Padding consistente em todos os lados. Border radius suave nas bordas. Margem vertical separa de elementos adjacentes.

## Fechamento

Prop closable adiciona botao de fechar no canto. OnClose callback executado ao fechar. Alerta removido do DOM apos fechar. Animacao fade out suaviza transicao.
