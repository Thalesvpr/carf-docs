---
modules: [GEOAPI, REURBCAD]
epic: performance
---

# US-070: Geolocalização de Fotos

Como analista, quero visualizar a localização geográfica de cada foto no mapa para que contexto espacial de onde cada imagem foi capturada seja claro facilitando análise territorial, onde a funcionalidade deve extrair automaticamente coordenadas GPS de metadados EXIF de fotos quando disponíveis, garantindo renderização de pin ou marcador no mapa para cada foto geolocalizada, permitindo que click no pin abra preview da foto correspondente criando navegação bidirecional entre mapa e galeria. Esta funcionalidade é implementada pelo módulo GEOWEB com visualização de fotos no mapa consumindo GEOAPI através do endpoint GET /api/units/{id}/photos que retorna latitude e longitude quando disponíveis nos metadados EXIF, sem requisitos funcionais específicos mas relacionada à visualização espacial de documentação. Os critérios de aceitação incluem extração automática de coordenadas GPS de metadados EXIF durante processamento de upload de fotos, armazenamento de latitude e longitude associadas a cada foto em campos dedicados no banco de dados, retorno de coordenadas junto com dados da foto no endpoint GET /api/units/{id}/photos, renderização de marcadores (pins ícones de câmera) no mapa nas posições correspondentes a fotos geolocalizadas, diferenciação visual de pins de fotos versus polígonos de unidades através de ícone e cor distintos, tooltip ao hover sobre pin mostrando thumbnail miniatura da foto e data de captura, click em pin abrindo lightbox ou painel lateral com preview da foto em resolução completa, camada toggle permitindo mostrar ou ocultar pins de fotos no mapa conforme preferência do analista, indicação clara quando foto não possui geolocalização (EXIF GPS não disponível), e navegação bidirecional permitindo acessar foto pelo mapa e visualizar localização da foto no mapa a partir da galeria. A rastreabilidade conecta esta user story ao endpoint GET /api/units/{id}/photos com inclusão de coordenadas lat/lon, garantindo análise espacial integrada de documentação fotográfica.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
