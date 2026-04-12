---
type: leaf
status: review
updated: 2026-02-07
---

# BottomSheet

Componente de painel inferior deslizante nativo para interacoes contextuais no mapa.

## Props

Prop open boolean controla visibilidade do bottom sheet. Prop onOpenChange callback invocado quando estado de abertura muda. Prop snapPoints array de percentuais define posicoes de parada do sheet. Prop children conteudo renderizado dentro do sheet. Prop handleComponent componente customizado opcional para alca de arraste.

## Snap Points

Snap points padrao configurados em 25%, 50% e 90% da altura da tela. Sheet ancora na posicao mais proxima ao soltar gesto de arraste. Primeiro snap point define altura inicial ao abrir. Ultimo snap point define expansao maxima antes de tela cheia.

## Gestos

PanGestureHandler captura arraste vertical na alca e conteudo. Spring animation suaviza transicao entre snap points. Arraste para baixo alem do primeiro snap point fecha o sheet. Velocidade do gesto influencia snap point destino para interacao natural.

## Overlay

Backdrop semi-transparente escurece conteudo atras do sheet quando aberto. Toque no backdrop fecha sheet invocando onOpenChange com false. Opacidade do backdrop anima proporcionalmente a altura do sheet. Backdrop nao renderiza quando sheet fechado para performance.

## Acessibilidade

Sheet recebe accessibilityRole adjustable para indicar natureza interativa. AccessibilityLabel descreve conteudo do painel para leitores de tela. Gesto de arraste comunica posicao percentual via accessibilityValue. Foco move para conteudo do sheet ao abrir.

## Estilizacao

Classes NativeWind aplicam bg-background rounded-t-xl ao container. Handle padrao renderiza barra cinza w-10 h-1 centralizada no topo. Shadow-lg aplica sombra superior para profundidade visual. Dark mode ajusta cores via dark: prefix.
