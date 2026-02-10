---
type: leaf
status: review
updated: 2026-02-07
---

# AlertDialog

Componente de dialogo nativo para confirmacoes bloqueantes que requerem acao do usuario.

## Props

Prop open boolean controla visibilidade do dialogo. Prop onOpenChange callback invocado quando estado de abertura muda. Prop title texto do titulo exibido no topo do dialogo. Prop description texto descritivo explicando contexto da acao. Prop confirmLabel texto do botao de confirmacao. Prop cancelLabel texto do botao de cancelamento. Prop onConfirm callback executado ao confirmar acao. Prop onCancel callback executado ao cancelar. Prop variant aceita default ou destructive definindo estilo do botao de confirmacao.

## Variantes

Variante default exibe botao de confirmacao com bg-primary para acoes padrao. Variante destructive exibe botao de confirmacao com bg-destructive vermelho para acoes perigosas como exclusao. Botao de cancelamento mantem estilo outline em ambas variantes.

## Comportamento

Modal nativo impede interacao com conteudo abaixo enquanto aberto. Backdrop escurecido nao fecha ao toque, forcando decisao explicita. Botao de cancelamento e confirmacao sao unicas formas de fechar. Back button no Android executa acao de cancelamento.

## Acessibilidade

Prop accessibilityRole definido como alertdialog comunicando natureza bloqueante. Titulo e descricao lidos automaticamente ao abrir para leitores de tela. Foco capturado dentro do dialogo impedindo navegacao para conteudo atras. Botao de cancelamento recebe foco inicial para seguranca.

## Estilizacao

Classes NativeWind aplicam bg-background rounded-xl ao container do dialogo. Titulo usa text-lg font-semibold centralizado. Descricao usa text-muted-foreground para contraste secundario. Botoes alinhados horizontalmente na base com gap-3.
