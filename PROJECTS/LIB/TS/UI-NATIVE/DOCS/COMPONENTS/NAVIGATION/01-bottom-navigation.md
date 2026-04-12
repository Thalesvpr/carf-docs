---
type: leaf
status: review
updated: 2026-02-07
---

# BottomNavigation

Componente de navegacao inferior nativo com tabs adaptados por role do usuario.

## Props

Prop role aceita enum Role de @carf/tscore definindo perfil do usuario logado. Prop items array de objetos com key, label, icon e screen definindo tabs disponiveis. Prop activeItem key do tab ativo atualmente. Prop onItemPress callback invocado com key do tab ao pressionar.

## Configuracao por Role

FIELD_COORDINATOR visualiza 4 tabs: Mapa, Unidades, Equipe e Perfil para gestao completa de campo. FIELD_CADASTRATOR nao exibe bottom navigation pois acessa mapa diretamente como tela principal. ADMIN visualiza tabs adaptados para gestao administrativa. Role determina items visiveis filtrando array de tabs configurado.

## Tab Items

Cada tab renderiza icone e label centralizados verticalmente. Tab ativo destaca com cor primaria no icone e texto. Tab inativo exibe cor mutada para contraste com ativo. Badge numerico opcional sobre icone para notificacoes pendentes.

## Posicionamento

SafeAreaView garante visibilidade acima do safe area inferior do dispositivo. Borda superior sutil separa navegacao do conteudo principal. Altura fixa com padding para area de toque confortavel. Posicionamento absoluto na base da tela sobre conteudo.

## Acessibilidade

Container recebe accessibilityRole tablist para contexto de navegacao. Cada tab recebe accessibilityRole tab com estado selected para tab ativo. AccessibilityLabel combina label e badge count quando presente. Navegacao por foco percorre tabs sequencialmente da esquerda para direita.

## Estilizacao

Classes NativeWind aplicam bg-background border-t border-border ao container. Tabs distribuidos uniformemente com flex-1 por item. Icones usam tamanho 24 com Lucide React Native. Dark mode ajusta cores via dark: prefix.
