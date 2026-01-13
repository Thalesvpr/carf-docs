---
modules: [GEOWEB]
epic: performance
---

# UC-010-FA-001: Adicionar WMTS

Fluxo alternativo do UC-010 Configurar Camadas WMS desviando no passo 4 onde ao invés de selecionar tipo WMS (raster dinâmico), ADMIN seleciona radio button WMTS (Web Map Tile Service) expandindo formulário revelando campos adicionais específicos para tiles pré-renderizados incluindo dropdown TileMatrixSet listando esquemas de pirâmide de zoom padrões como GoogleMapsCompatible (Web Mercator usado por Google Maps OSM compatível com EPSG:3857), GlobalCRS84Pixel (WGS84 lat/lon), InspireCrs84Quad (padrão europeu INSPIRE), permitindo seleção conforme servidor oferece indicado no GetCapabilities XML, dropdown Format selecionando image/png (transparência suportada ideal para sobreposições mantendo qualidade) ou image/jpeg (menor tamanho de arquivo compressão com perda ideal para ortofotos sem necessidade de canal alfa), sistema ao testar conexão executa GetCapabilities WMTS parseando XML extraindo TileMatrixSet available e Formats suportados pré-populando dropdowns com opções válidas evitando configuração manual incorreta, ao salvar constrói URL de tiles seguindo template RESTful padrão WMTS `{url}/{layer}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.{format}` permitindo MapLibre GL JS carregar tiles diretamente com performance otimizada usando cache de navegador e carregamento paralelo de múltiplos tiles, vantagem sobre WMS inclui performance muito superior pois tiles são pré-gerados servidos estaticamente via CDN sem processamento servidor em cada request, ideal para ortofotos de alta resolução que em WMS gerariam timeouts por renderização pesada, usado tipicamente para integrar Google Earth Engine Mapbox Satellite ESRI World Imagery que fornecem WMTS público.

**Ponto de Desvio:** Passo 4 do UC-010 (seleção de tipo)

**Retorno:** Camada WMTS configurada com TileMatrixSet e Format específicos

---

**Última atualização:** 2025-12-30
