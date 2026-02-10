---
type: leaf
status: review
updated: 2026-02-08
---

# Header

Componente de cabecalho de tela nativo com botao de voltar, titulo, acoes contextuais e indicador de conectividade. Substitui o header padrao do React Navigation com design e funcionalidades especificas do REURBCAD.

## Props

| Prop | Tipo TS | Obrigatorio | Padrao | Descricao |
|:-----|:--------|:------------|:-------|:----------|
| title | string | sim | - | Texto do titulo exibido no centro |
| showBackButton | boolean | nao | true | Exibe botao de voltar a esquerda |
| onBack | funcao | nao | navigation.goBack | Callback ao pressionar voltar |
| actions | array de HeaderAction | nao | vazio | Acoes contextuais a direita |
| showSyncButton | boolean | nao | false | Exibe botao de sincronizacao |
| onSync | funcao | nao | - | Callback ao pressionar sync |
| showNotificationBadge | boolean | nao | false | Exibe badge de notificacoes |
| notificationCount | number | nao | 0 | Contagem de notificacoes pendentes |
| showOfflineIndicator | boolean | nao | true | Exibe indicador de conectividade abaixo do header |
| isOnline | boolean | nao | true | Estado de conectividade para o indicador |

Cada HeaderAction contem icon (string referenciando icone Lucide), onPress (callback), accessibilityLabel (string) e badge (number opcional para contagem).

## Comportamento

O header renderiza em tres zonas: esquerda com botao de voltar (chevron-left), centro com titulo truncado em texto unico e direita com ate tres acoes contextuais. O botao de voltar invoca onBack ou navigation.goBack como fallback. Acoes contextuais renderizam como icones pressionaveis com area de toque minima de 44x44 pontos conforme WCAG 2.1 AA.

O botao de sincronizacao, quando visivel, exibe icone de refresh-cw que anima rotacao durante sincronizacao ativa. O badge de notificacoes renderiza circulo vermelho com contagem sobre o icone de sino (bell), omitido quando contagem e zero.

Quando showOfflineIndicator e true e isOnline e false, o OfflineIndicator do @carf/ui-native renderiza barra vermelha logo abaixo do header informando ausencia de conectividade. Esta integracao garante que o usuario sempre veja o estado de conexao independente da tela em que estiver.

## Diferenca entre iOS e Android

No iOS, o titulo centraliza respeitando safe area top e usa fonte SF Pro com peso semibold. No Android, o titulo alinha a esquerda apos o botao de voltar seguindo Material Design e usa fonte Roboto Medium. A altura do header e 44 pontos no iOS e 56 dp no Android, ambos com padding horizontal de 16. O botao de voltar usa chevron no iOS e arrow-left no Android.

## Acessibilidade

O header recebe accessibilityRole header para leitores de tela identificarem a regiao de navegacao. O botao de voltar tem accessibilityLabel "Voltar" e accessibilityHint "Retorna para tela anterior". Cada acao contextual requer accessibilityLabel descritivo. Badge de notificacoes anuncia contagem via accessibilityValue. O indicador offline anuncia mudanca de estado via accessibilityLiveRegion polite.

## Estilizacao

Classes NativeWind aplicam bg-background border-b border-border ao container. Titulo usa text-lg font-semibold text-foreground. Icones usam tamanho 24 com cor text-foreground. Badge usa bg-destructive text-destructive-foreground rounded-full. Dark mode ajusta todas as cores via dark: prefix do NativeWind.
