---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: maintainability
---

# US-043: Selecionar Fotos da Galeria

Como agente de campo, quero anexar fotos já existentes na galeria do dispositivo para que a flexibilidade no processo de documentação seja maior, permitindo utilizar imagens capturadas anteriormente em outras aplicações ou momentos, onde a funcionalidade deve fornecer acesso à galeria de fotos do dispositivo com suporte a seleção múltipla de imagens, garantindo que as fotos selecionadas sejam comprimidas automaticamente antes do upload para otimizar uso de dados móveis e armazenamento, permitindo que o agente complemente a documentação visual da unidade com imagens já disponíveis no dispositivo. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com processamento de imagens e sincronização gerenciada pelo GEOAPI através do endpoint POST /api/units/{id}/photos durante o processo de sync, incluindo validação de formatos de arquivo e extração de metadados EXIF quando disponíveis nas imagens importadas. Os critérios de aceitação incluem acesso nativo à galeria de fotos do dispositivo sem necessidade de permissões excessivas, capacidade de selecionar múltiplas imagens simultaneamente através de interface intuitiva, compressão automática de imagens antes do upload mantendo qualidade adequada para documentação, exibição de preview das imagens selecionadas antes de confirmar anexação, preservação de metadados EXIF disponíveis nas imagens originais incluindo geolocalização quando presente, feedback visual do processo de compressão e preparação das imagens, limite configurável de tamanho e quantidade de imagens por unidade, e sincronização automática das imagens anexadas quando houver conectividade disponível. A rastreabilidade conecta esta user story ao RF-123 (Importação de Fotos da Galeria) e ao UC-004 (Cadastrar Unidade no Campo), garantindo flexibilidade na documentação visual das unidades cadastradas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
