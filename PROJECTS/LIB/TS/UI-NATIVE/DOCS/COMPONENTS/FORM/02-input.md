---
type: leaf
status: review
updated: 2026-01-24
---

# Input

Componente de campo de texto com estilos consistentes e integracao com formularios.

## Props

Prop placeholder exibe texto quando vazio. Prop value controla conteudo em modo controlado. Prop onChangeText recebe callback com novo valor. Prop error aceita string de erro exibida abaixo. Prop disabled impede edicao com estilo visual.

## Ref Forwarding

Componente usa forwardRef para expor TextInput nativo. Permite integracao com react-hook-form via register. Metodos focus e blur disponiveis via ref. Necessario para navegacao de campos via keyboard.

## Estados Visuais

Estado normal exibe borda neutra com fundo claro. Estado focus destaca borda com cor primary. Estado error exibe borda destructive com mensagem abaixo. Estado disabled reduz opacidade e impede interacao.

## Acessibilidade

Prop accessibilityLabel descreve proposito do campo. Erro anunciado automaticamente via accessibilityLiveRegion. Placeholder nao substitui label para leitores de tela. Keyboard type define teclado apropriado para conteudo.

## Tipos de Teclado

Prop keyboardType aceita default, email-address, numeric ou phone-pad. Prop secureTextEntry oculta caracteres para senhas. Prop autoComplete sugere preenchimento automatico. Prop returnKeyType define botao de acao do teclado.

## Estilizacao

Classes base aplicam padding, borda e tipografia consistentes. Classes customizadas via className estendem estilo. Dark mode ajusta cores de fundo e borda. Focus ring usa outline-primary.
