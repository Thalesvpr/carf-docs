---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-081: Gerar Termo de Legitimação (PDF)

Como gestor do sistema de regularização fundiária, quero gerar termo de legitimação em formato PDF para que documentos oficiais sejam emitidos de forma automatizada e padronizada, garantindo conformidade legal e agilidade processual. O sistema deve permitir a configuração de templates personalizáveis onde dados cadastrais da unidade habitacional, informações do titular, coordenadas geográficas e histórico do processo de legitimação sejam automaticamente preenchidos no documento, incluindo funcionalidade de assinatura digital integrada para validação jurídica do termo emitido. A funcionalidade deve oferecer tanto opção de download imediato quanto armazenamento persistente no banco de dados vinculado ao processo específico de legitimação, permitindo recuperação futura para fins de auditoria, consulta ou reemissão. Os critérios de aceitação incluem a implementação de template configurável com campos dinâmicos, preenchimento automático de dados extraídos do sistema GEOAPI, mecanismo de assinatura digital compatível com ICP-Brasil ou equivalente, e dupla funcionalidade de download instantâneo e armazenamento no repositório de documentos do processo. Esta User Story está relacionada ao RF-179 e UC-009, sendo implementada no backend GEOAPI através do endpoint POST /api/legitimation/processes/{id}/generate-term e no frontend GEOWEB com interface de geração e visualização de documentos, garantindo rastreabilidade completa do processo de legitimação fundiária dentro do Epic 9: Legitimação Fundiária. O status atual é implemented, indicando funcionalidade já disponível em produção com testes unitários e de integração validados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
