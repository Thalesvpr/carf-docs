---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-062: Geocodificação de Endereço

Como analista, quero buscar um endereço textual e navegar automaticamente para sua localização no mapa para que a navegação geográfica seja rápida sem necessidade de conhecer coordenadas, onde a funcionalidade deve fornecer search bar com autocomplete sugerindo endereços conforme usuário digita, garantindo integração com API de geocodificação (Google Maps Nominatim ou similar) para converter endereço em coordenadas, permitindo que ao selecionar resultado o mapa automaticamente execute zoom e centralize na localização correspondente. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de busca consumindo GEOAPI através do endpoint GET /api/geocode?address={query} que intermedia chamadas a serviços externos de geocodificação, sem requisitos funcionais específicos por ser funcionalidade auxiliar de navegação. Os critérios de aceitação incluem disponibilidade de search bar destacada na interface do mapa para entrada de endereços textuais, autocomplete mostrando sugestões de endereços conforme usuário digita a partir do terceiro caractere, integração com serviço de geocodificação externo (Google Geocoding API Nominatim MapBox Geocoding), exibição de lista de resultados quando múltiplas localizações correspondem à busca, seleção de resultado acionando navegação automática do mapa para coordenadas retornadas, zoom automático para nível apropriado (tipicamente 16-18) ao localizar endereço, marcador temporário indicando ponto geocodificado no mapa, histórico de buscas recentes acessível para repetir navegações anteriores, e tratamento gracioso de casos onde endereço não é encontrado exibindo mensagem clara ao usuário. A rastreabilidade conecta esta user story ao endpoint GET /api/geocode?address={query}, garantindo navegação eficiente por referências de endereço em vez de coordenadas geográficas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
