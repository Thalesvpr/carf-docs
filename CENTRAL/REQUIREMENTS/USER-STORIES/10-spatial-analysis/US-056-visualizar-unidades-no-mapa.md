---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-056: Visualizar Unidades no Mapa

Como analista, quero visualizar unidades cadastradas plotadas no mapa interativo para que a visão geográfica da distribuição e status das unidades seja clara, onde a funcionalidade deve renderizar polígonos das geometrias das unidades com cores diferenciadas por status (DRAFT PENDING APPROVED REJECTED), garantindo que hover sobre polígono exiba tooltip com dados básicos (código nome titular status), permitindo que click no polígono abra painel lateral com detalhes completos da unidade incluindo performance otimizada para renderizar mais de 1000 unidades simultaneamente sem lag perceptível. Esta funcionalidade é implementada pelo módulo GEOWEB utilizando bibliotecas de mapeamento como Mapbox ou Leaflet com clustering e virtualização, consumindo dados do GEOAPI através do endpoint GET /api/units que retorna GeoJSON, integrada ao RF-053 (Visualização de Unidades no Mapa). Os critérios de aceitação incluem renderização de polígonos de todas unidades visíveis no viewport atual do mapa, diferenciação visual por cores baseada em status (verde para APPROVED amarelo para PENDING azul para DRAFT vermelho para REJECTED), exibição de tooltip ao passar mouse sobre polígono mostrando minimamente code name holder_name status, abertura de painel lateral de detalhes ao clicar em polígono contendo informações completas e opções de edição, performance garantida suportando renderização de mais de 1000 unidades simultaneamente sem lag na interação, clustering automático em níveis de zoom distantes agrupando unidades próximas com contador, desagrupamento progressivo conforme zoom in até renderizar polígonos individuais, e suporte a seleção múltipla de unidades através de shift+click ou desenho de área de seleção. A rastreabilidade conecta esta user story ao RF-053 (Visualização Geográfica de Unidades), garantindo interface intuitiva para análise espacial e gestão de unidades cadastradas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
