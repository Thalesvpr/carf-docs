---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: scalability
---

# US-068: OCR em Documentos

Como analista, quero extrair automaticamente texto de documentos escaneados ou imagens para que busca textual seja possível mesmo em arquivos não nativamente pesquisáveis, onde a funcionalidade deve executar OCR (Optical Character Recognition) automaticamente em PDFs escaneados e imagens JPG/PNG após upload, garantindo que texto extraído seja indexado em sistema de busca full-text, permitindo search por conteúdo textual de documentos retornando resultados relevantes mesmo quando texto original era apenas imagem. Esta funcionalidade é implementada pelo módulo GEOAPI utilizando biblioteca de OCR (Tesseract Azure Computer Vision ou similar) processada assincronamente através do endpoint POST /api/documents/{id}/ocr que agenda job de extração, sem requisitos funcionais específicos mas relacionada à gestão avançada de documentos. Os critérios de aceitação incluem processamento automático de OCR acionado após upload de documento PDF ou imagem (JPG PNG), detecção automática de documentos que necessitam OCR (PDFs escaneados versus PDFs nativos com texto selecionável), execução assíncrona de OCR em background através de job queue para não bloquear interface, extração de texto utilizando engine OCR (Tesseract OCR Azure Computer Vision Google Cloud Vision), armazenamento de texto extraído associado ao documento original em campo searchable_content ou similar, indexação de texto extraído em mecanismo de busca full-text (Elasticsearch PostgreSQL FTS ou similar), interface de busca permitindo search por conteúdo textual retornando documentos cujo OCR contém termos buscados, destaque visual de termos encontrados dentro do preview do documento quando possível, indicação de status de processamento OCR (PENDING PROCESSING COMPLETED FAILED) visível na interface, e retry automático ou manual de OCR em caso de falha no processamento. A rastreabilidade conecta esta user story ao endpoint POST /api/documents/{id}/ocr, garantindo capacidade de busca avançada mesmo em documentação não estruturada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
