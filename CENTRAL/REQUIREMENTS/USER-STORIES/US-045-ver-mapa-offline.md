---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-045: Ver Mapa Offline

Como agente de campo, quero visualizar mapa base offline no dispositivo mobile para que eu consiga navegar e localizar unidades mesmo sem conexão com internet, onde a funcionalidade deve permitir o download prévio de tiles de mapa para uma área geográfica configurável correspondente à comunidade ou região de trabalho, garantindo disponibilidade de níveis de zoom entre 14 e 18 que são adequados para navegação em campo e identificação de unidades individuais, permitindo que o agente trabalhe em áreas remotas ou com conectividade limitada sem comprometer a capacidade de visualização espacial. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile utilizando bibliotecas de mapeamento offline como Mapbox ou Leaflet com plugins de cache local, processada pelo GEOAPI no backend para gestão de tiles e áreas de download, incluindo estimativa de espaço necessário e controle de expiração de cache. Os critérios de aceitação incluem capacidade de baixar tiles de mapa previamente quando conectado selecionando área geográfica específica (comunidade ou bairro), configuração de níveis de zoom disponíveis offline entre zoom 14 (visão de bairro) e zoom 18 (visão de lote individual), exibição de estimativa de espaço de armazenamento necessário antes de iniciar download, barra de progresso visual durante download dos tiles com opção de pausar e retomar, funcionamento completo do mapa offline incluindo pan e zoom dentro dos níveis baixados, indicador visual claro diferenciando modo online e offline, gestão de espaço permitindo excluir mapas offline de áreas não mais utilizadas, e atualização automática de tiles quando conectado caso nova versão esteja disponível no servidor. A rastreabilidade conecta esta user story ao RF-183 (Visualização de Mapa Offline) e ao UC-004 (Cadastrar Unidade no Campo), garantindo capacidade de trabalho autônomo sem dependência de conectividade.

---

**Última atualização:** 2025-12-30
