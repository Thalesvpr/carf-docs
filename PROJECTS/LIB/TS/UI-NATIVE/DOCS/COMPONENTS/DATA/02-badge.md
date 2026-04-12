---
type: leaf
status: review
updated: 2026-01-24
---

# Badge

Componente de etiqueta pequena para categorias, contadores e status.

## Props

Prop children aceita texto ou numero exibido. Prop variant aceita default, secondary, outline ou destructive. Prop size aceita sm ou default controlando padding e fonte.

## Variantes

Variante default usa bg-primary com texto branco para destaque. Variante secondary usa bg-secondary com texto escuro para informacao neutra. Variante outline usa borda sem preenchimento para sutileza. Variante destructive usa bg-destructive vermelho para alertas.

## Uso como Contador

Numero como children exibe contador compacto. Prop max limita valor maximo exibido, mostrando + apos. Exemplo: max 99 exibe 99+ para valores maiores. Zero opcional via prop showZero.

## Posicionamento

Badge usado inline com texto em listas. Badge posicionado absolutamente sobre icones para notificacoes. Componente BadgeWrapper facilita posicionamento sobre children. Corner prop define canto: top-right, top-left, bottom-right, bottom-left.

## Acessibilidade

AccessibilityLabel descreve significado da badge. Contador inclui contexto como 5 mensagens nao lidas. Status badges anunciam estado atual. Cor nao e unica forma de comunicar informacao.

## Animacao

Prop pulse adiciona animacao pulsante para atencao. Prop bounce anima entrada com bounce. Transicoes suaves em mudancas de valor. Animacoes respeitam prefers-reduced-motion.
