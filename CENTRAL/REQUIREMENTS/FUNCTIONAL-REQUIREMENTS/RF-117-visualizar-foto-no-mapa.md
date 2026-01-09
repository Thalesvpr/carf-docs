---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: usability
---

# RF-117: Visualizar Foto no Mapa

Este requisito estabelece que fotos com coordenadas geográficas geotag devem ser exibidas como marcadores clicáveis no mapa interativo, onde cada foto que possui geometria Point é renderizada como pin ou ícone diferenciado permitindo visualização espacial da localização onde foto foi capturada. Os marcadores devem ser clicáveis, onde ao clicar o sistema exibe popup contendo miniatura da foto junto com informações básicas como data de captura tipo e descrição se disponível, permitindo identificação rápida do conteúdo sem abrir visualização completa. O popup deve incluir link direto para galeria completa ou visualização ampliada da foto, facilitando navegação do contexto espacial para análise detalhada da imagem com um único clique adicional. O sistema deve agrupar marcadores em clusters quando múltiplas fotos estão próximas em níveis de zoom distantes, expandindo automaticamente ao aproximar zoom para evitar sobreposição visual e melhorar usabilidade em áreas com alta densidade fotográfica. A funcionalidade deve ser implementada no módulo GEOWEB através de camada específica de fotos no mapa que pode ser ativada ou desativada conforme necessidade do usuário.

---

**Última atualização:** 2025-12-30