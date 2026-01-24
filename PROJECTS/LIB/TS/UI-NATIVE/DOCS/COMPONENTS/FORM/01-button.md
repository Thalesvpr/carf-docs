---
type: leaf
status: review
updated: 2026-01-24
---

# Button

Componente de botao com variantes visuais, estados de loading e acessibilidade.

## Props

Prop variant aceita default, outline, ghost ou destructive definindo estilo visual. Prop size aceita sm, default ou lg controlando dimensoes. Prop disabled desabilita interacao com opacidade reduzida. Prop loading exibe spinner e desabilita durante processamento.

## Variantes

Variante default usa bg-primary com texto branco para acoes principais. Variante outline usa borda sem preenchimento para acoes secundarias. Variante ghost remove borda e fundo para acoes terciarias. Variante destructive usa bg-destructive vermelho para acoes perigosas.

## Estados

Estado normal permite interacao com feedback visual ao pressionar. Estado disabled reduz opacidade e ignora toques. Estado loading exibe ActivityIndicator centralizado substituindo children. Estados combinam via prop spread.

## Acessibilidade

Prop accessibilityRole definido como button automaticamente. Prop accessibilityLabel recebe texto descritivo da acao. Estado disabled comunica-se via accessibilityState disabled true. Loading anuncia estado de carregamento para leitores de tela.

## Estilizacao

Classes NativeWind aplicam estilos responsivos. Tailwind classes em className prop estendem estilo base. Active state usa active: prefix para feedback de pressao. Dark mode inverte cores via dark: prefix.
