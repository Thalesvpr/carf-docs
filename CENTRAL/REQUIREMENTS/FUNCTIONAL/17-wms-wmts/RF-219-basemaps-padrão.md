---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
---

# RF-219: Basemaps Padrao

## Descricao

Sistema deve oferecer conjunto predefinido de basemaps essenciais garantindo funcionalidade imediata sem configuracao adicional. OpenStreetMap como mapa vetorial colaborativo com nomenclatura de ruas e POIs e opcao padrao carregada automaticamente. Google Satellite (quando licenciado) proporcionando imagens de alta resolucao para identificacao visual de edificacoes e limites fisicos. Opcao de Mapa em Branco para visualizar exclusivamente dados cadastrais sem basemap contextual. Todos os basemaps configurados com cache otimizado, atribuicao de direitos autorais, limites de zoom apropriados e sistemas de coordenadas garantindo alinhamento perfeito com dados vetoriais cadastrais.

## Criterios de Aceitacao

1. OpenStreetMap como padrao
2. Google Satellite (se licenciado)
3. Opcao de Mapa em Branco
4. Cache de tiles otimizado
5. Atribuicao de direitos autorais

## Rastreabilidade

- Modulos: GEOWEB
- Requisitos dependentes: RF-220
