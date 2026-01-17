---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-044: Cadastrar Titular no Campo

Como agente de campo, quero cadastrar dados do titular durante a visita à unidade para que os dados completos sejam coletados em um único momento de contato com o morador, onde a funcionalidade deve fornecer um formulário simplificado otimizado para preenchimento offline contendo campos essenciais de identificação do titular, garantindo que seja possível capturar foto de documentos como RG ou CNH para posterior verificação e processamento OCR, permitindo validação local de CPF através de algoritmo de dígitos verificadores sem necessidade de conectividade com bases externas. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com armazenamento local e processamento pelo GEOAPI no backend, incluindo validações de campos obrigatórios e formatação automática de documentos (CPF CNPJ RG). Os critérios de aceitação incluem disponibilidade de formulário simplificado funcionando completamente offline com campos essenciais (nome completo CPF RG data_nascimento telefone), capacidade de capturar foto de documentos de identificação (RG CNH) diretamente pela câmera ou galeria, validação matemática de CPF em tempo real sem necessidade de conexão verificando dígitos verificadores, máscara automática de formatação para campos de documento (XXX.XXX.XXX-XX para CPF), feedback visual de validação indicando campos válidos e inválidos antes de salvar, opção de vincular o titular recém-cadastrado imediatamente à unidade em edição, armazenamento temporário local dos dados do titular até sincronização com servidor, e sincronização automática dos dados e fotos de documentos quando conectividade estiver disponível. A rastreabilidade conecta esta user story ao RF-184 (Cadastro de Titular no Campo) e ao UC-004 (Cadastrar Unidade no Campo), garantindo coleta completa de informações cadastrais durante a visita de campo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
