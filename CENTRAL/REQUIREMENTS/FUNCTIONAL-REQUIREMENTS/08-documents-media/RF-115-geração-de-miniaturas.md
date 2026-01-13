---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# RF-115: Geração de Miniaturas

Este requisito estabelece que o sistema deve gerar automaticamente miniaturas thumbnails de fotos no momento do upload para otimizar performance em interfaces de listagem e galeria, onde miniaturas são versões reduzidas pré-renderizadas que carregam rapidamente evitando necessidade de redimensionar imagens originais no cliente. As miniaturas devem ter dimensões de 200x200 pixels em formato quadrado, onde o sistema aplica crop inteligente centralizando área de interesse ou redimensiona mantendo proporções com preenchimento de espaço vazio se necessário, garantindo consistência visual em grids de galeria. A geração deve ocorrer automaticamente ao fazer upload durante pipeline de processamento backend, onde thumbnail é criado junto com compressão e extração de EXIF como parte de fluxo único otimizado. As miniaturas devem ser armazenadas separadamente da imagem original no storage object S3/MinIO, tipicamente em prefixo ou bucket diferente, permitindo políticas de cache e CDN específicas para thumbnails que são acessados com muito mais frequência. O sistema deve retornar URLs separadas para imagem original e thumbnail nos endpoints da API, permitindo que frontend carregue versão apropriada conforme contexto de uso. A funcionalidade deve ser implementada no módulo GEOAPI como parte do processamento de upload.

---

**Última atualização:** 2025-12-30