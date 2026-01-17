---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# US-082: Exportar Mapa como Imagem

Como analista de geoprocessamento, quero exportar o mapa atual visualizado na interface como arquivo de imagem em formato PNG para que apresentações técnicas, relatórios impressos e documentação de campo possam ser elaborados com representações visuais precisas do cadastro territorial. A funcionalidade deve disponibilizar botão de exportação claramente identificado na interface do mapa onde o usuário possa acionar a geração da imagem, incluindo configuração de resolução ajustável para atender diferentes necessidades de qualidade (visualização em tela, impressão, apresentação de alta definição). O sistema deve preservar o estado atual do mapa no momento da exportação, garantindo que zoom, camadas ativas, filtros aplicados e seleções de features sejam fielmente representados na imagem gerada, permitindo documentação exata do contexto analisado. Os critérios de aceitação incluem presença de botão Export acessível na interface do mapa, seletor de resolução com opções predefinidas (baixa, média, alta) ou configuração customizada em DPI, e manutenção completa do estado visual incluindo nível de zoom, camadas visíveis, filtros ativos e features selecionados. Esta User Story pertence ao Epic 10: Relatórios e Exportação, sendo implementada no backend GEOAPI para processamento de renderização cartográfica e no frontend GEOWEB com interface de configuração e download, garantindo capacidade de documentação visual do trabalho de cadastramento territorial. O status atual é implemented, indicando disponibilidade em produção com validação através de testes automatizados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
