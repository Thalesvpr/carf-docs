---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: cross-cutting
---

# RF-161: Visualizar Pontos no Mapa

O sistema renderiza pontos topográficos importados diretamente no mapa interativo através de marcadores visuais que exibem o código identificador de cada ponto, permitindo aos usuários técnicos localizar e identificar rapidamente os vértices do levantamento cadastral. Ao interagir com os marcadores através de clique ou toque, o sistema exibe um popup contendo informações detalhadas incluindo coordenadas planas X Y, altitude Z e metadados associados ao ponto, facilitando a verificação e validação dos dados topográficos sem necessidade de consultar o arquivo original. Os pontos são organizados em uma camada dedicada e independente das demais features geográficas, possibilitando controle granular de visibilidade e permitindo que o usuário ative ou desative a exibição dos pontos topográficos conforme necessário durante análises espaciais ou edição de unidades territoriais. Esta separação em camadas específicas também otimiza o desempenho do mapa ao trabalhar com grandes volumes de pontos de levantamento, garantindo fluidez na navegação mesmo em projetos cadastrais extensos com milhares de coordenadas registradas.

---

**Última atualização:** 2025-12-30
