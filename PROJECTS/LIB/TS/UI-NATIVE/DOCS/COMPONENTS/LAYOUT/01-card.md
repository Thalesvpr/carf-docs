---
type: leaf
status: review
updated: 2026-02-07
---

# Card

Componente container nativo para agrupamento visual de conteudo relacionado.

## Props

Prop children recebe conteudo interno do card. Prop variant aceita default, elevated ou outlined definindo estilo visual. Prop onPress callback opcional que torna card pressionavel com feedback visual. Prop className permite extensao de estilos via NativeWind.

## Variantes

Variante default usa fundo bg-card com borda sutil e rounded-lg para uso geral. Variante elevated adiciona shadow-md com elevacao nativa criando profundidade visual. Variante outlined usa borda mais proeminente sem sombra para separacao clara do fundo.

## Composicao

Componente CardHeader renderiza area superior com titulo e descricao opcional. Componente CardContent renderiza area principal com padding consistente para conteudo. Componente CardFooter renderiza area inferior para acoes e botoes. Composicao via children permite layouts flexiveis sem sub-componentes obrigatorios.

## Estados

Estado normal exibe card estatico quando onPress nao definido. Estado pressionavel adiciona feedback visual ao toque quando onPress presente. Estado pressed reduz opacidade momentaneamente via active:opacity-90. Dark mode inverte cores de fundo e borda.

## Acessibilidade

Card pressionavel recebe accessibilityRole button automaticamente. AccessibilityLabel descreve conteudo do card para leitores de tela. Feedback tatil ao pressionar comunica interatividade. Cards nao pressionaveis atuam como containers semanticos.

## Estilizacao

Classes NativeWind aplicam rounded-lg e overflow-hidden como base. Padding interno via CardContent garante espacamento consistente. ClassName prop no container permite customizacao de margens e largura. Dark mode ajusta fundo via dark:bg-card.
