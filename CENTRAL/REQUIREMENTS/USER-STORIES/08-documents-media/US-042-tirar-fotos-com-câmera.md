---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: maintainability
---

# US-042: Tirar Fotos com Câmera

Como agente de campo, quero tirar fotos de unidades diretamente pelo aplicativo mobile para que a documentação visual seja anexada ao cadastro da unidade durante a coleta de dados em campo, onde a funcionalidade deve fornecer acesso direto à câmera do dispositivo com captura de metadados EXIF incluindo geolocalização automática da foto, garantindo que cada imagem capturada seja salva inicialmente como miniatura local para economizar armazenamento do dispositivo e posteriormente enviada em resolução completa durante o processo de sincronização com o servidor, permitindo que o agente documente visualmente aspectos relevantes da unidade como fachada, numeração, condições construtivas e ocupação. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com armazenamento local e sincronização gerenciada pelo GEOAPI através do endpoint POST /api/units/{id}/photos durante o processo de sync, incluindo compressão inteligente de imagens e validação de formatos aceitos (JPG PNG HEIC). Os critérios de aceitação incluem acesso nativo à câmera do dispositivo mobile sem necessidade de sair do aplicativo, captura automática de coordenadas GPS no EXIF da foto quando disponível, salvamento de miniatura comprimida localmente para visualização rápida offline, upload automático da imagem em resolução completa durante sincronização quando houver conectividade, exibição de preview imediato após captura com opções de aceitar ou descartar, capacidade de adicionar múltiplas fotos à mesma unidade, rotação automática da imagem baseada na orientação do dispositivo, e feedback de progresso durante upload de fotos grandes. A rastreabilidade conecta esta user story ao RF-122 (Captura de Fotos com Câmera) e ao UC-004 (Cadastrar Unidade no Campo), garantindo documentação visual completa das unidades cadastradas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
