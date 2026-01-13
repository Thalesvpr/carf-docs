---
modules: [GEOWEB]
epic: performance
---

# RF-046: Configurar Camadas WMS para Comunidade

Usuários com role ADMIN podem configurar camadas WMS/WMTS de base específicas para visualização de comunidade onde URL de serviço WMS configurável através de formulário validando conectividade e compatibilidade com padrões OGC antes de salvar, seleção de layers disponíveis no serviço WMS apresentada através de interface de checklist ou seleção múltipla onde sistema consulta GetCapabilities do serviço extrai lista de layers disponíveis e permite ADMIN escolher quais exibir como base ou overlay para comunidade, ordem de renderização configurável através de drag-and-drop ou controles de ordenação numérica onde layers superiores renderizados por cima de inferiores permitindo composição visual adequada e controle de visibilidade, implementação em módulos GEOWEB e GEOAPI com formulário de configuração preview de camadas selecionadas antes de salvar persistência de configuração por comunidade (ou global para tenant) e integração com cliente de mapa carregando dinamicamente WMS layers configurados.

---

**Última atualização:** 2025-12-30
