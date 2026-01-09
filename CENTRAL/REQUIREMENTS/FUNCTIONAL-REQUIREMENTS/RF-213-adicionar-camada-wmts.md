---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# RF-213: Adicionar Camada WMTS

O sistema possibilita adição de camadas WMTS (Web Map Tile Service) que fornecem tiles pré-renderizados otimizados para desempenho superior comparado a WMS tradicional, sendo especialmente adequadas para basemaps de alta resolução como imagens de satélite ou mapas topográficos detalhados que exigem renderização rápida em múltiplos níveis de zoom. A configuração requer URL do servidor WMTS e permite seleção de TileMatrixSet apropriado que define esquema de pirâmide de tiles incluindo sistemas de coordenadas, níveis de zoom disponíveis e dimensões de tiles, garantindo compatibilidade entre serviço remoto e cliente de mapeamento utilizado pelo sistema. A interface permite configurar identificador do layer específico a ser consumido quando servidor oferece múltiplos layers através do mesmo endpoint, formato de imagem preferencial (PNG para transparência, JPEG para tamanho reduzido), e parâmetros adicionais como dimensões temporais para serviços que oferecem séries históricas de imagens. As camadas WMTS configuradas proporcionam experiência de navegação mais fluida que WMS devido a caching natural do formato tiled, onde tiles individuais são carregados independentemente e podem ser reutilizados quando usuário retorna a áreas previamente visualizadas, reduzindo drasticamente tempo de carregamento e consumo de banda em comparação com requisições WMS dinâmicas que regeneram imagens completamente a cada pan ou zoom.

---

**Última atualização:** 2025-12-30
