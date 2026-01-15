---
modules: [GEOAPI, GEOWEB]
epic: maintainability
---

# US-065: Upload de Documentos

Como analista, quero anexar documentos diversos a unidades cadastradas para que evidências documentais sejam armazenadas centralizadamente vinculadas ao cadastro, onde a funcionalidade deve suportar formatos comuns de documentos incluindo PDF DOCX XLSX JPG e PNG, garantindo limite de tamanho máximo de 10MB por arquivo para controle de armazenamento, permitindo upload múltiplo de vários arquivos simultaneamente e preview integrado de documentos PDF diretamente na interface. Esta funcionalidade é implementada pelo módulo GEOWEB com componente de upload e preview consumindo GEOAPI através do endpoint POST /api/units/{id}/documents que processa e armazena arquivos, integrada ao RF-063 (Gestão de Documentos Anexos) para documentação completa de unidades. Os critérios de aceitação incluem interface de upload acessível na tela de detalhes da unidade permitindo anexar documentos, suporte a formatos PDF DOCX XLSX JPG PNG com validação de tipo de arquivo no frontend e backend, limite de tamanho máximo de 10MB por arquivo individual com mensagem clara ao exceder, capacidade de selecionar e fazer upload de múltiplos arquivos simultaneamente em uma operação, barra de progresso visual mostrando andamento de upload de cada arquivo, preview integrado de documentos PDF diretamente no navegador sem necessidade de download, thumbnails para imagens JPG PNG mostrando visualização prévia reduzida, metadados automáticos associados a cada documento (nome original tamanho data_upload usuário_upload), validação de virus/malware através de scanning antes de aceitar arquivo definitivamente, e organização de documentos anexados em lista ou grid na interface da unidade. A rastreabilidade conecta esta user story ao RF-063 (Anexação de Documentos) e ao endpoint POST /api/units/{id}/documents, garantindo capacidade de documentação rica e completa das unidades cadastradas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
