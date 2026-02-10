---
type: leaf
status: review
updated: 2026-02-07
---

# Tabs

Componente de abas nativo com suporte a swipe para navegacao entre paineis de conteudo.

## Props

Prop tabs aceita array de objetos com key, label e content definindo cada aba. Prop activeTab define key da aba ativa atualmente. Prop onTabChange callback invocado com key da nova aba ao trocar. Prop swipeable boolean habilita navegacao por gesto de swipe horizontal entre paineis.

## Tab Bar

Tab bar renderiza ScrollView horizontal com botoes de aba alinhados. Aba ativa exibe indicador visual inferior com bg-primary. Scroll horizontal permite mais abas que a largura da tela. Animacao de transicao do indicador acompanha mudanca de aba.

## Paineis

Painel ativo renderiza conteudo correspondente abaixo da tab bar. Swipeable usa gesto horizontal para transicao entre paineis adjacentes. Paineis adjacentes pre-renderizados para transicao fluida. Conteudo de painel inativo desmontado para economia de memoria quando nao swipeable.

## Estados

Estado ativo destaca aba com cor primaria e indicador inferior. Estado inativo exibe aba com cor mutada sem indicador. Transicao entre estados usa animacao de spring para fluidez.

## Acessibilidade

Tab bar recebe accessibilityRole tablist para contexto de navegacao. Cada aba recebe accessibilityRole tab com estado selected para aba ativa. Painel de conteudo recebe accessibilityRole tabpanel vinculado a aba correspondente. Navegacao por foco percorre abas sequencialmente.

## Estilizacao

Classes NativeWind aplicam estilos responsivos a tab bar e paineis. Indicador ativo usa h-0.5 bg-primary com animacao de posicao. Dark mode ajusta cores via dark: prefix. ClassName extende container principal.
