---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-063: Imprimir Mapa

Como analista, quero imprimir ou exportar o mapa atual com suas camadas e filtros ativos para que documentação impressa ou digital seja gerada para relatórios e apresentações, onde a funcionalidade deve fornecer botão "Imprimir" acessível que captura estado atual do mapa, garantindo capacidade de exportar em formatos PNG ou PDF mantendo qualidade visual adequada, permitindo que zoom nível de detalhe e filtros aplicados sejam preservados exatamente como visualizados na tela. Esta funcionalidade é implementada pelo módulo GEOWEB utilizando bibliotecas de captura de canvas do mapa (html2canvas ou API nativa de export do provider de mapas), sem necessidade de endpoints backend específicos além de possível processamento server-side de PDF. Os critérios de aceitação incluem disponibilidade de botão "Imprimir/Exportar" facilmente acessível na barra de ferramentas do mapa, opção de exportar visualização atual como imagem PNG de alta resolução, opção alternativa de exportar como documento PDF com possível inclusão de metadados (título data escala), preservação fiel do zoom atual do mapa na imagem/PDF exportado, manutenção de filtros ativos aplicados às camadas visíveis no momento da exportação, inclusão opcional de legenda explicando cores e símbolos utilizados no mapa, opção de incluir escala gráfica e norte geográfico na exportação, configuração opcional de tamanho e orientação (retrato paisagem) para PDF, e download automático do arquivo gerado ou preview antes de salvar. A rastreabilidade não possui requisitos funcionais ou endpoints específicos, sendo funcionalidade de interface para documentação e comunicação de análises espaciais.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
