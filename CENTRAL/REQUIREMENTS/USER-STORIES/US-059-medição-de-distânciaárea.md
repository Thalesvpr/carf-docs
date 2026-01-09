---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-059: Medição de Distância e Área

Como analista, quero medir distâncias entre pontos e calcular áreas de polígonos diretamente no mapa para que análise geográfica seja precisa sem necessidade de ferramentas externas, onde a funcionalidade deve fornecer ferramenta de medição ativável permitindo desenhar linhas para distância ou polígonos para área, garantindo exibição de resultados em unidades métricas (metros para distância e metros quadrados para área), permitindo que múltiplas medições sejam mantidas simultaneamente no mapa para comparação visual. Esta funcionalidade é implementada pelo módulo GEOWEB utilizando bibliotecas de cálculo geográfico como Turf.js para computação client-side de distâncias e áreas geodésicas, sem necessidade de endpoints backend específicos. Os critérios de aceitação incluem disponibilidade de ferramenta de medição de distância ativável via botão na barra de ferramentas do mapa, modo de medição permitindo clicar em pontos sequenciais para traçar linha com cálculo automático de distância total, exibição em tempo real da distância acumulada em metros ou quilômetros conforme escala apropriada, ferramenta alternativa de medição de área permitindo desenhar polígono fechado com cálculo automático, exibição de área calculada em metros quadrados (m²) ou hectares (ha) conforme magnitude, suporte a múltiplas medições simultâneas no mapa cada uma identificada visualmente e numerada, tooltip ou label fixo mostrando valor medido junto à geometria desenhada, e botão "Limpar medições" permitindo remover todas medições do mapa de uma vez. A rastreabilidade não possui requisitos funcionais ou endpoints específicos, sendo funcionalidade auxiliar de análise implementada completamente no frontend.

---

**Última atualização:** 2025-12-30
