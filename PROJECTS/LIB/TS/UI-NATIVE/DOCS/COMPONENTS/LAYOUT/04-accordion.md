---
type: leaf
status: review
updated: 2026-02-07
---

# Accordion

Componente de paineis expansiveis nativo com animacao de abertura e fechamento.

## Props

Prop items aceita array de objetos com key, trigger e content definindo cada painel. Prop type aceita single ou multiple controlando quantos paineis podem estar abertos simultaneamente. Prop defaultOpen aceita key ou array de keys de paineis inicialmente abertos.

## Comportamento

Tipo single permite apenas um painel aberto, fechando anterior ao abrir novo. Tipo multiple permite abertura independente de qualquer quantidade de paineis. Toque no trigger alterna estado de expansao do painel correspondente. Conteudo expande e contrai com animacao suave via LayoutAnimation.

## Animacao

LayoutAnimation configureNext aplica transicao de spring ao expandir e contrair. Altura do conteudo anima de zero ate tamanho natural do conteudo. Icone chevron rotaciona 180 graus acompanhando estado de expansao. Duracao padrao de 300ms para transicao natural.

## Estados

Estado collapsed oculta conteudo com chevron apontando para baixo. Estado expanded exibe conteudo com chevron rotacionado para cima. Trigger mantem estilo consistente independente do estado de expansao. Bordas entre items mantem separacao visual.

## Acessibilidade

Trigger recebe accessibilityRole button com accessibilityState expanded indicando estado. AccessibilityHint informa que toque alterna expansao do conteudo. Conteudo expandido recebe foco automaticamente para leitores de tela. Navegacao sequencial percorre triggers e conteudos visiveis.

## Estilizacao

Classes NativeWind aplicam borda inferior entre items para separacao. Trigger usa padding p-4 com flex-row justify-between para layout. Conteudo usa padding p-4 pt-0 para alinhamento com trigger. Dark mode ajusta cores via dark: prefix.
