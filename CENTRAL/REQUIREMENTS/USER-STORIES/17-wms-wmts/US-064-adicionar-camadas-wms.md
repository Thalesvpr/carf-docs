---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-064: Adicionar Camadas WMS

Como gestor, quero adicionar camadas WMS (Web Map Service) externas ao mapa para que dados geográficos de fontes externas (IBGE prefeituras órgãos ambientais) sejam visualizados integrados com dados do sistema, onde a funcionalidade deve permitir cadastrar URL do serviço WMS especificando layers desejadas e sistema de referência espacial (SRS), garantindo preview da camada antes de salvar configuração para validação visual, permitindo toggle on/off de cada camada cadastrada e configuração de transparência (opacity) para sobreposição adequada com outras camadas. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de gerenciamento de camadas externas consumindo GEOAPI através do endpoint POST /api/wms-layers para persistir configurações, integrada ao RF-212 (Integração com Camadas WMS) e UC-010 (Configurar Camadas Externas). Os critérios de aceitação incluem formulário de cadastro de camada WMS solicitando URL do serviço nome da layer e código SRS (EPSG:4326 EPSG:31983 etc), validação de conectividade testando GetCapabilities do serviço WMS antes de salvar, preview visual da camada em painel lateral antes de confirmar adição ao mapa, salvamento de configuração da camada no backend via POST /api/wms-layers para uso por todos usuários, listagem de camadas WMS cadastradas com controles individuais de visibilidade (toggle on/off), slider de transparência (0-100%) para cada camada permitindo ajuste de opacity para melhor visualização, ordenação de camadas controlando z-index e precedência de renderização, opção de editar ou remover camadas WMS previamente cadastradas, e tratamento de erros quando serviço WMS está indisponível ou retorna erro. A rastreabilidade conecta esta user story ao RF-212 (Suporte a Camadas WMS) UC-010 (Configurar Camadas Externas) e endpoint POST /api/wms-layers, garantindo integração flexível com fontes externas de dados geográficos.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
