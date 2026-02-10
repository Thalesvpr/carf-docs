---
type: leaf
status: review
updated: 2026-02-07
---

# OfflineIndicator

Componente indicador de status de conectividade com feedback visual semantico.

## Props

Prop status aceita online, offline ou syncing definindo estado atual de conectividade. Prop pendingCount numero opcional de operacoes pendentes de sincronizacao.

## Estados Visuais

Status online exibe barra verde no topo da tela indicando conexao ativa. Status offline exibe barra vermelha no topo com mensagem de sem conexao. Status syncing exibe barra amarela com animacao de pulse durante sincronizacao. PendingCount exibido junto a mensagem de syncing quando presente.

## Animacao

Barra aparece e desaparece com animacao de slide vertical do topo. Status syncing aplica animacao de pulse continua para indicar atividade. Transicao entre estados usa animacao de fade para suavidade. Barra online desaparece automaticamente apos 3 segundos de conexao estavel.

## Posicionamento

Barra renderiza acima de todo conteudo via posicionamento absoluto no topo. SafeAreaView garante visibilidade abaixo da status bar do sistema. Altura fixa de h-8 com conteudo centralizado verticalmente. Conteudo abaixo nao sofre shift de layout durante transicoes.

## Acessibilidade

AccessibilityLiveRegion polite anuncia mudancas de status para leitores de tela. AccessibilityLabel descritivo inclui estado e contagem de pendencias. Cor nao e unica forma de comunicar estado com texto complementar sempre presente. Role status definido para semantica correta.

## Estilizacao

Cores semanticas seguem convencao verde online, amarelo syncing, vermelho offline. Classes NativeWind aplicam z-50 para sobreposicao de conteudo. Texto branco com font-medium para legibilidade sobre fundo colorido. Dark mode mantem mesmas cores semanticas por contraste adequado.
