---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-220: Trocar Basemap

## Descricao

Sistema deve disponibilizar seletor intuitivo de basemap permitindo usuario alternar entre mapas base disponiveis incluindo OpenStreetMap para mapa vetorial com nomenclatura de ruas, imagens de satelite para analise de uso do solo, mapas topograficos com curvas de nivel, ou mapas tematicos customizados. Troca ocorre instantaneamente via clique sem recarregar pagina. Sistema persiste preferencia de basemap via cookie ou local storage garantindo que acessos futuros carreguem automaticamente ultimo basemap utilizado. Funcionalidade reconhece que diferentes tarefas beneficiam-se de diferentes contextos cartograficos adaptando visualizacao conforme necessidade.

## Criterios de Aceitacao

1. Seletor intuitivo de basemaps
2. Troca instantanea sem recarregar
3. Persistencia de preferencia local
4. Multiplas opcoes (OSM, satelite, topo)
5. Restauracao automatica em proximo acesso

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-219
