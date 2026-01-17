---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-060: Camadas de Mapa Base

Como analista, quero trocar a camada base do mapa entre diferentes estilos de visualização para que a análise seja otimizada conforme contexto, onde a funcionalidade deve oferecer opções de camadas base incluindo minimamente Street (ruas e logradouros) Satellite (imagem de satélite) e Hybrid (satélite com sobreposição de ruas), garantindo troca instantânea entre camadas sem recarregar página, permitindo que preferência do usuário seja salva persistentemente para sessões futuras. Esta funcionalidade é implementada pelo módulo GEOWEB utilizando providers de tile como Mapbox OpenStreetMap ou Google Maps com gerenciamento de camadas em memória, sem necessidade de endpoints backend específicos além de possível armazenamento de preferência do usuário. Os critérios de aceitação incluem disponibilidade de controle de camadas base acessível via botão ou dropdown na interface do mapa, opções mínimas de camadas sendo Street para visualização de ruas e logradouros Satellite para imagem aérea de satélite e Hybrid combinando satélite com overlay de ruas, troca instantânea de camada ao selecionar opção sem necessidade de recarregar página ou perder contexto de zoom e posição, indicação visual clara de qual camada base está atualmente ativa, persistência de preferência do usuário salvando escolha de camada em localStorage ou perfil de usuário, carregamento automático da camada preferida ao abrir mapa em novas sessões, e fallback gracioso para camada padrão caso camada preferida falhe ao carregar. A rastreabilidade não possui requisitos funcionais ou endpoints específicos, sendo funcionalidade de interface implementada no frontend com suporte de providers externos de tiles.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
