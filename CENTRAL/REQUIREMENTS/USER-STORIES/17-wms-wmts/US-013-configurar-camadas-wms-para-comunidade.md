---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-013: Configurar Camadas WMS para Comunidade

Como gestor, quero configurar camadas WMS específicas para comunidade para que visualização seja contextualizada, onde o sistema permite associar serviços Web Map Service externos a comunidades específicas fornecendo contexto geográfico relevante como imagens de satélite, mapas cadastrais ou outras camadas temáticas específicas da região. O cenário principal de uso inicia quando um gestor com permissões adequadas acessa as configurações de uma comunidade e adiciona uma nova camada WMS fornecendo a URL do serviço WMS compatível com padrão OGC, permitindo que o sistema valide a conectividade com o serviço, apresente a lista de layers disponíveis no WMS, e o gestor selecione quais layers específicos devem ser disponibilizados para visualização no contexto daquela comunidade. Os critérios de aceitação incluem o cadastro de URL de serviço WMS com validação de conectividade e compatibilidade com padrão OGC WMS 1.1.0 ou superior, a seleção de layers específicos da lista retornada pelo GetCapabilities do serviço WMS, o vínculo claro da configuração de camadas WMS a uma community específica no sistema, e a funcionalidade de toggle on/off que permite ativar ou desativar camadas sem removê-las da configuração. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/communities/{id}/wms-layers para gerenciar configuração de WMS por comunidade) e GEOWEB (interface de configuração de comunidade com formulário de WMS e preview de layers), garantindo rastreabilidade com RF-212 (Configuração de Camadas WMS por Comunidade) e UC-010 (Caso de Uso de Administração de Comunidades), onde camadas configuradas aparecem automaticamente no mapa quando usuários acessam dados daquela comunidade específica, incluindo cache de GetCapabilities para performance e tratamento de serviços WMS temporariamente indisponíveis.

---

**Última atualização:** 2025-12-30