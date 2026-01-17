---
modules: [REURBCAD]
epic: usability
---

# RF-110: Geotagging de Fotos

Este requisito especifica que o sistema deve automaticamente extrair e armazenar coordenadas geográficas de fotos que contenham metadados EXIF com informações de GPS, onde o processo ocorre durante o upload através de leitura dos metadados EXIF embutidos no arquivo de imagem. O sistema deve implementar extração automática de latitude e longitude dos campos GPS correspondentes no EXIF, validando que os valores estejam em formato e range válidos antes de processar, garantindo que coordenadas corrompidas ou inválidas sejam tratadas apropriadamente. As coordenadas extraídas devem ser armazenadas como geometria do tipo Point utilizando tipos geoespaciais do PostGIS, permitindo queries espaciais eficientes e integração com funcionalidades de mapeamento do sistema. Se a foto não contiver dados de GPS nos metadados EXIF, o campo de geometria permanece nulo mas o upload não é rejeitado, permitindo atribuição manual posterior de localização se necessário. Esta funcionalidade é particularmente valiosa para fotos capturadas por aplicativos mobile onde GPS está habilitado, vinculando automaticamente imagens a localizações de campo. A extração e armazenamento devem ocorrer nos módulos GEOAPI durante processamento de upload e REURBCAD para fotos capturadas em dispositivos móveis.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
