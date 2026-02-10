---
type: leaf
status: review
updated: 2026-02-07
---

# Textarea

Componente de campo de texto multi-linha nativo com auto-crescimento opcional.

## Props

Prop value texto atual do campo controlado externamente. Prop onChangeText callback invocado a cada alteracao de texto. Prop placeholder texto guia exibido quando campo vazio. Prop maxLength limita numero maximo de caracteres com contador visual. Prop numberOfLines define altura inicial em numero de linhas visiveis. Prop disabled desabilita edicao com opacidade reduzida. Prop error string exibe mensagem de erro abaixo do campo. Prop label texto descritivo acima do campo. Prop autoGrow boolean permite expansao automatica conforme conteudo cresce.

## Comportamento

Campo renderiza como TextInput com multiline true nativo. AutoGrow ajusta altura dinamicamente conforme usuario digita novas linhas. MaxLength exibe contador de caracteres restantes no canto inferior direito. Scroll interno ativa quando conteudo excede area visivel sem autoGrow.

## Estados

Estado normal permite edicao com borda sutil e fundo bg-input. Estado focused aplica borda primaria e ring visual indicando foco ativo. Estado disabled reduz opacidade e impede edicao. Estado error aplica borda vermelha com mensagem descritiva abaixo.

## Acessibilidade

Prop accessibilityLabel recebe texto do label automaticamente. AccessibilityHint informa limite de caracteres quando maxLength definido. Estado disabled comunica-se via accessibilityState. Leitores de tela anunciam campo como area de texto editavel.

## Estilizacao

Classes NativeWind aplicam min-h-[100px] como altura minima padrao. Padding interno garante legibilidade com p-3. Dark mode ajusta cores via dark: prefix. ClassName prop permite extensao de estilos base.
