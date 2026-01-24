---
type: leaf
status: review
updated: 2026-01-24
---

# Switch

Componente de alternancia entre dois estados com animacao fluida.

## Props

Prop checked controla estado em modo controlado. Prop onCheckedChange recebe callback com novo valor booleano. Prop disabled impede interacao. Prop label exibe texto descritivo explicando o que o switch controla.

## Estados Visuais

Estado off exibe track cinza com thumb na esquerda. Estado on exibe track primary com thumb na direita. Transicao anima thumb deslizando horizontalmente. Estado disabled reduz opacidade em ambos estados.

## Animacao

React Native Reanimated fornece animacao performatica. Thumb desliza com spring physics natural. Track muda cor com fade suave. Animacao respeita prefers-reduced-motion.

## Acessibilidade

AccessibilityRole definido como switch automaticamente. AccessibilityState comunica checked como booleano. Label descreve efeito de alternar. Toque em qualquer parte do componente alterna estado.

## Uso Comum

Preferencias de usuario como dark mode ou notificacoes. Toggles de feature flags em configuracoes. Formularios com campos opcionais on/off. Filtros rapidos em listas.

## Estilizacao

Track usa bg-muted quando off e bg-primary quando on. Thumb sempre branco com sombra sutil. Tamanho configuravel via size prop. Classes customizadas estendem container via className.
