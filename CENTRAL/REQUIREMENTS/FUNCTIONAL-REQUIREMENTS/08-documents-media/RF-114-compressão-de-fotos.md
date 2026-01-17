---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-114: Compressão de Fotos

Este requisito especifica que o sistema deve automaticamente comprimir fotos durante processo de upload para otimizar armazenamento e performance, onde a compressão ocorre no backend antes de salvar arquivo final no storage. O sistema deve redimensionar imagens que excedam 2048 pixels em qualquer dimensão, mantendo proporções originais e garantindo que fotos de alta resolução sejam reduzidas a tamanho gerenciável sem perda significativa de qualidade visual para uso em aplicações web e mobile. A compressão deve aplicar qualidade de 80% no algoritmo JPEG, balanceando redução de tamanho de arquivo com preservação de qualidade suficiente para análise e documentação, onde valor de 80% tipicamente produz arquivos significativamente menores mantendo qualidade aceitável. Crítico é que o processo preserve metadados EXIF originais incluindo informações de GPS, data/hora de captura e configurações de câmera, garantindo que dados importantes para geotagging e rastreabilidade não sejam perdidos durante compressão. O sistema deve processar compressão de forma assíncrona se possível evitando timeout em uploads, fornecendo feedback de progresso para usuário. A funcionalidade deve ser implementada no módulo GEOAPI durante pipeline de processamento de upload de fotos.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
