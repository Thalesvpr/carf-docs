---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-066: Visualizar Documentos

Como analista, quero visualizar documentos previamente anexados a unidades para que análise de evidências documentais seja completa e conveniente, onde a funcionalidade deve exibir lista organizada de documentos com miniaturas representativas, garantindo que click em documento abra preview em modal ou painel lateral sem sair da tela atual, permitindo download do arquivo original quando necessário para uso externo ou compartilhamento. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de galeria de documentos consumindo GEOAPI através dos endpoints GET /api/units/{id}/documents para listar e GET /api/documents/{id}/download para obter arquivos, integrada ao RF-064 (Visualização de Documentos Anexos) para acesso conveniente a evidências. Os critérios de aceitação incluem exibição de lista ou grid de documentos anexados na tela de detalhes da unidade, miniaturas visuais representativas para cada tipo de documento (ícone PDF ícone Word preview de imagem), informações de metadados visíveis para cada documento (nome tamanho data_upload responsável), click em documento abrindo preview em modal ou painel lateral sem navegar para outra página, preview integrado no navegador para PDFs e imagens sem necessidade de download, botão de download disponível permitindo salvar arquivo original localmente, navegação entre múltiplos documentos dentro do preview sem fechar modal, suporte a zoom e paginação para documentos PDF multipáginas, e indicação clara de loading durante carregamento de previews de arquivos grandes. A rastreabilidade conecta esta user story ao RF-064 (Acesso a Documentos) e aos endpoints GET /api/units/{id}/documents e GET /api/documents/{id}/download, garantindo acesso eficiente a documentação anexada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
