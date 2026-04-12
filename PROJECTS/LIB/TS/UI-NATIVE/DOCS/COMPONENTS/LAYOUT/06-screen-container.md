---
type: leaf
status: review
updated: 2026-02-08
---

# ScreenContainer

Componente container de tela que encapsula SafeAreaView, StatusBar e KeyboardAvoidingView em uma unica abstraccao para uso consistente em todas as telas do REURBCAD. Elimina a necessidade de configurar manualmente safe areas, status bar e comportamento de teclado em cada tela.

## Props

| Prop | Tipo TS | Obrigatorio | Padrao | Descricao |
|:-----|:--------|:------------|:-------|:----------|
| children | ReactNode | sim | - | Conteudo da tela |
| statusBarStyle | "light" ou "dark" | nao | "dark" | Estilo da status bar do sistema |
| statusBarColor | string | nao | bg-background | Cor de fundo da status bar (Android) |
| edges | array de string | nao | ["top", "bottom"] | Bordas com safe area padding |
| scrollable | boolean | nao | false | Envolve conteudo em ScrollView quando true |
| padding | boolean | nao | true | Aplica padding horizontal padrao p-4 |
| className | string | nao | - | Classes NativeWind adicionais no container |

## Comportamento

O ScreenContainer compoe SafeAreaView do react-native-safe-area-context como wrapper externo, garantindo que o conteudo respeite notch, status bar e home indicator em dispositivos iOS e Android. O StatusBar e configurado via props statusBarStyle e statusBarColor, com translucent true no Android para layout edge-to-edge.

O KeyboardAvoidingView envolve o conteudo com behavior "padding" no iOS e "height" no Android, deslocando o conteudo automaticamente quando o teclado virtual aparece para evitar que campos de formulario fiquem ocultos. Quando scrollable e true, um ScrollView com keyboardShouldPersistTaps "handled" permite que toques em areas fora do teclado o fechem naturalmente.

O padding horizontal padrao de 16px (p-4) garante margens consistentes em todas as telas, podendo ser desabilitado via prop padding false para telas que precisam de conteudo edge-to-edge como o mapa.

## Diferenca entre iOS e Android

No iOS, a StatusBar nao ocupa espaco no layout; o SafeAreaView compensa com padding top automatico. No Android, a StatusBar ocupa espaco; o componente define translucent true e compensa com StatusBar.currentHeight como padding. O KeyboardAvoidingView usa behavior "padding" no iOS (desloca conteudo para cima) e "height" no Android (reduz altura disponivel), ambos com keyboardVerticalOffset calculado a partir da altura do header quando presente.

## Acessibilidade

O container nao interfere na arvore de acessibilidade, atuando como wrapper transparente. Conteudo scrollable anuncia natureza rolavel para leitores de tela. StatusBar style garante contraste adequado dos icones do sistema sobre o fundo da tela.

## Estilizacao

Classes NativeWind aplicam flex-1 bg-background como base do container. SafeAreaView usa edges configuravel para controle granular de quais bordas recebem padding seguro. Dark mode inverte bg-background automaticamente via configuracao de tema NativeWind.
