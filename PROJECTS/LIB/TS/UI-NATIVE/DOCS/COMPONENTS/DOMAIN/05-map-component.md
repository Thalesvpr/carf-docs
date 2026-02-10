---
type: leaf
status: review
updated: 2026-02-07
---

# MapComponent

Wrapper nativo de react-native-maps com suporte a layers, clustering e demarcacao de unidades.

## Props

Prop region objeto com latitude, longitude e deltas definindo area visivel do mapa. Prop markers array de pontos com coordenadas e metadata para exibicao no mapa. Prop polygons array de poligonos com coordenadas definindo limites de unidades e comunidades. Prop layers array de Layer tipado controlando camadas visiveis do mapa. Prop onMarkerPress callback invocado com marker ao tocar. Prop onPolygonPress callback invocado com polygon ao tocar. Prop clustering boolean habilita agrupamento automatico de markers proximos. Prop orthoTileUrl string opcional de URL para tiles de ortofoto.

## Layers

Sistema de camadas permite alternar visibilidade de markers, poligonos e tiles. Layer de unidades exibe poligonos de demarcacao com cores de status. Layer de pontos exibe markers de coleta GPS e vertices de poligonos. Layer de ortofoto sobrepoe tiles de imagem aerea sobre mapa base. Controle de layers via painel lateral deslizante.

## Clustering

Markers proximos agrupam automaticamente quando clustering habilitado. Cluster exibe contagem de markers agrupados com tamanho proporcional. Zoom in expande clusters revelando markers individuais. Algoritmo de clustering otimizado para grandes quantidades de pontos.

## Draw Mode

Modo de desenho permite demarcar limites de unidades tocando vertices no mapa. Poligono em construcao exibe vertices editaveis com linhas conectoras. Confirmacao finaliza poligono e calcula area automaticamente. Edicao permite arrastar vertices de poligonos existentes.

## Acessibilidade

Markers recebem accessibilityLabel com descricao do ponto. Gestos de zoom alternativo via botoes de mais e menos. Poligonos anunciam dados da unidade ao receber foco. Mapa anuncia regiao visivel ao mover.

## Integracao

Ortofoto tiles carregam sob demanda com cache local para uso offline. Poligonos sincronizam com WatermelonDB para persistencia local. Coordenadas usam projecao EPSG:4326 compativel com IBGE. Integra com expo-location para posicao atual do usuario.
