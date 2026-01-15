---
modules: [GEOWEB]
epic: performance
---

# RF-053: Visualizar Unidade no Mapa

Sistema deve exibir unidade no mapa web interativo com geometria colorida por status de workflow onde renderização de polígono utiliza biblioteca cartográfica (Leaflet OpenLayers Mapbox) com performance otimizada para grandes quantidades de features através de clustering ou tiling, cores por status implementam esquema visual intuitivo onde DRAFT exibido em cinza ou amarelo indicando trabalho em progresso PENDING em laranja aguardando revisão APPROVED em verde confirmando conclusão REJECTED em vermelho indicando reprovação CHANGES_REQUESTED em azul solicitando ajustes facilitando identificação visual rápida de estado de unidades, popup ou painel lateral exibindo dados resumidos ao clicar em polígono incluindo código endereço tipo área titulares status atual e ações rápidas (editar completo visualizar detalhes aprovar/rejeitar se MANAGER) com loading eficiente de informações sob demanda, implementação em módulos GEOWEB e REURBCAD com mapa base configurável layers vetoriais otimizados controles de zoom/pan ferramentas de seleção múltipla filtros visuais por status e sincronização com listagem tabular permitindo navegação integrada mapa-lista.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
