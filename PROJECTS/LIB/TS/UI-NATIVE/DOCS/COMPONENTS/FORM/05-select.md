---
type: leaf
status: review
updated: 2026-02-07
---

# Select

Componente dropdown nativo para selecao de opcao unica com BottomSheet no iOS.

## Props

Prop items aceita array de objetos com label e value representando opcoes disponiveis. Prop value define item selecionado atualmente. Prop onValueChange callback invocado com novo valor ao selecionar opcao. Prop placeholder exibe texto guia quando nenhum valor selecionado. Prop disabled desabilita interacao com opacidade reduzida. Prop error string exibe mensagem de erro abaixo do campo. Prop label texto descritivo acima do campo.

## Variantes

Variante default usa fundo bg-input com borda sutil para formularios padrao. Variante outlined usa borda mais proeminente sem preenchimento para destaque visual. Ambas exibem chevron-down indicando natureza expansivel do componente.

## Comportamento

Toque abre BottomSheet no iOS com picker nativo para selecao fluida. No Android usa Picker nativo do sistema operacional. Lista de opcoes renderiza com scroll quando excede area visivel. Selecao de opcao fecha automaticamente o picker e atualiza valor.

## Acessibilidade

Prop accessibilityRole definido como combobox automaticamente. AccessibilityLabel combina label e valor selecionado para leitores de tela. Estado disabled comunica-se via accessibilityState disabled true. Opcoes anunciam posicao na lista para navegacao.

## Estilizacao

Classes NativeWind aplicam estilos responsivos ao container. Estado de erro aplica borda vermelha e exibe mensagem. Dark mode ajusta cores via dark: prefix. Chevron icon posicionado absolutamente a direita.
