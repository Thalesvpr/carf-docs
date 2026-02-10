---
type: leaf
status: review
updated: 2026-02-07
---

# CommunityCard

Componente nativo que exibe resumo de comunidade/nucleo urbano com dados do dominio CARF.

## Props

Prop community aceita objeto Community tipado de @carf/tscore com dados da comunidade. Prop onPress callback opcional que torna card pressionavel para navegacao. Prop variant aceita compact ou expanded controlando nivel de detalhe exibido.

## Variantes

Variante compact exibe nome da comunidade, badge de tipo e contagem de unidades em linha unica para uso em listas. Variante expanded exibe nome, tipo, contagem de unidades, area total e informacoes adicionais de localizacao para telas de detalhe.

## Dados Exibidos

Nome da comunidade renderiza como titulo principal com font-semibold. Badge de tipo exibe classificacao da comunidade usando StatusBadge. Contagem de unidades exibe total de unidades habitacionais cadastradas. Area total exibe metragem quadrada formatada na variante expanded. Localizacao exibe municipio e estado na variante expanded.

## Composicao

CommunityCard compoe internamente com Card container para estrutura visual. StatusBadge renderiza tipo da comunidade com cor semantica. Layout flex organiza informacoes em hierarquia visual clara. Variante compact otimiza para renderizacao em FlatList com altura fixa.

## Acessibilidade

AccessibilityLabel combina nome, tipo e contagem de unidades para leitores de tela. Card pressionavel recebe accessibilityRole button com accessibilityHint de navegacao. Informacoes visuais replicadas em texto acessivel para completude. Contraste de texto sobre fundo garante legibilidade.

## Estilizacao

Classes NativeWind aplicam bg-card rounded-lg com padding consistente. Variante compact usa p-3 para densidade em listas. Variante expanded usa p-4 com spacing entre secoes. Dark mode ajusta cores via dark: prefix.
