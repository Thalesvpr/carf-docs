---
type: leaf
status: review
updated: 2026-01-24
---

# Toast

Componente de notificacao temporaria exibida no topo ou fundo da tela.

## Props

Prop message exibe texto principal da notificacao. Prop variant aceita default, destructive, warning ou success. Prop duration define millisegundos ate auto-dismiss, padrao 3000. Prop action aceita objeto com label e onPress para acao opcional.

## Posicionamento

Prop position aceita top ou bottom definindo ancoragem. Toast desliza de fora da tela ao aparecer. Multiplos toasts empilham-se verticalmente. Ultimo toast sempre visivel no topo da pilha.

## Auto-Dismiss

Toast desaparece automaticamente apos duration. Prop persistent true mantem toast ate dismiss manual. Interacao do usuario pausa timer temporariamente. Timer reinicia quando interacao termina.

## Acao

Prop action renderiza botao ao lado direito. OnPress executa callback, geralmente undo. Toast permanece visivel durante acao. Dismiss ocorre apos acao completar.

## Acessibilidade

AccessibilityLiveRegion polite para anuncio nao intrusivo. Variante destructive usa assertive para urgencia. Acao focavel via navegacao de acessibilidade. Auto-dismiss anunciado antes de desaparecer.

## API Imperativa

Hook useToast retorna funcao show para exibir toasts programaticamente. Contexto ToastProvider envolve app fornecendo container. Show retorna id para dismiss programatico. Queue gerencia multiplas notificacoes.
