---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-212: Adicionar Camada WMS

## Descricao

Sistema deve permitir que usuarios com perfil ADMIN adicionem camadas WMS (Web Map Service) externas ao mapa interativo, possibilitando integracao de bases cartograficas oficiais de orgaos governamentais sem necessidade de download local. Interface de configuracao solicita URL do servidor WMS e executa requisicao GetCapabilities recuperando metadados como lista de layers, sistemas de coordenadas e extensao espacial. Para cada camada adicionada, administrador configura opacidade, z-index, nome amigavel e restricoes de visibilidade por role. Camadas configuradas ficam disponiveis no seletor para usuarios autorizados ativarem durante analises espaciais, enriquecendo contexto com informacoes como limites administrativos, hidrografia ou zoneamento urbano.

## Criterios de Aceitacao

1. Configuracao via URL com GetCapabilities automatico
2. Selecao de layers especificos do servidor
3. Configuracao de opacidade e z-index
4. Restricao de acesso por role
5. Disponibilidade no seletor de camadas

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-214
