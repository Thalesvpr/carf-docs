---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: performance
---

# RF-219: Basemaps Padrão

O sistema oferece conjunto predefinido de basemaps essenciais que garante funcionalidade imediata sem necessidade de configuração adicional de serviços externos, incluindo OpenStreetMap como mapa vetorial colaborativo que fornece nomenclatura detalhada de ruas, pontos de interesse e limites administrativos constantemente atualizados pela comunidade global, sendo opção padrão carregada automaticamente ao iniciar sistema. Quando projeto dispõe de licenciamento apropriado, sistema pode incluir Google Satellite proporcionando imagens de satélite de alta resolução que permitem identificação visual precisa de edificações, limites físicos de terrenos, características de vegetação e uso real do solo, sendo recurso valiosíssimo para validação de limites cadastrados e identificação de ocupações irregulares ou expansões não documentadas. Opção de Mapa em Branco é disponibilizada para contextos onde usuário deseja visualizar exclusivamente dados cadastrais do próprio sistema sem qualquer basemap contextual distraindo, sendo útil para análises focadas em geometrias puras, geração de mapas técnicos sem informação de fundo, ou situações de conectividade extremamente limitada onde carregamento de tiles externos seria inviável. Todos os basemaps padrão são configurados com parâmetros otimizados de cache, atribuição de direitos autorais conforme requisitos de cada provedor, limites de zoom apropriados que balanceiam detalhamento com desempenho, e sistemas de coordenadas corretamente especificados garantindo alinhamento perfeito entre basemap e dados vetoriais cadastrais sobrepostos, proporcionando experiência cartográfica profissional e confiável desde primeiro uso do sistema.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
