---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# US-069: Galeria de Fotos da Unidade

Como analista, quero visualizar todas as fotos anexadas a uma unidade em formato de galeria organizada para que visualização e análise de documentação fotográfica seja fácil e intuitiva, onde a funcionalidade deve exibir grid de miniaturas de todas fotos da unidade organizadas cronologicamente, garantindo que click em miniatura abra lightbox em tela cheia com foto em alta resolução, permitindo navegação sequencial entre fotos usando setas ou gestos sem fechar lightbox. Esta funcionalidade é implementada pelo módulo GEOWEB com componente de galeria e lightbox consumindo GEOAPI através do endpoint GET /api/units/{id}/photos que retorna lista de fotos com URLs, integrada ao RF-186 (Galeria de Fotos) para visualização eficiente de documentação visual. Os critérios de aceitação incluem exibição de grid responsivo de miniaturas de fotos na tela de detalhes da unidade, ordenação cronológica das fotos por data de captura ou upload (mais recentes primeiro ou último), miniaturas otimizadas (thumbnails) carregadas do servidor para performance em vez de imagens completas, click em miniatura abrindo lightbox modal em tela cheia exibindo foto em resolução completa, navegação entre fotos no lightbox usando setas direcionais (anterior próxima) ou swipe em mobile, exibição de contador indicando posição atual (exemplo "3 de 12") dentro do lightbox, botão de fechar lightbox retornando à visualização de grid, metadados visíveis no lightbox incluindo data de captura dimensões e tamanho do arquivo, opção de download da foto em resolução original diretamente do lightbox, e suporte a zoom dentro do lightbox para examinar detalhes da foto. A rastreabilidade conecta esta user story ao RF-186 (Interface de Galeria de Fotos) e ao endpoint GET /api/units/{id}/photos, garantindo visualização eficiente e profissional de documentação fotográfica das unidades.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
