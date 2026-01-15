---
modules: [GEOAPI]
epic: compatibility
---

# US-032: Visualizar Histórico de Titulares

Como analista, quero ver histórico de titulares de uma unidade para que eu rastreie transferências, onde o sistema mantém registro temporal completo de todos os titulares que já estiveram vinculados a cada unidade incluindo períodos de vigência e mudanças de titularidade, garantindo capacidade de rastrear evolução da situação fundiária ao longo do tempo. O cenário principal de uso ocorre quando analista acessa detalhes de uma unidade e visualiza seção dedicada ao histórico de titularidade apresentando timeline cronológica mostrando todos os titulares que já foram vinculados incluindo aqueles atualmente ativos e os históricos que foram desvinculados, permitindo compreensão da trajetória de propriedade e posse da unidade. Os critérios de aceitação incluem apresentação de lista cronológica de holders mostrando todos os titulares que já estiveram vinculados à unidade ordenados por data de vínculo, exibição de data de vínculo indicando quando titular foi associado à unidade e data de desvínculo quando aplicável mostrando quando relacionamento foi encerrado, e apresentação de percentual de propriedade histórico mostrando evolução das proporções de titularidade ao longo do tempo incluindo mudanças quando coproprietários foram adicionados ou removidos. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/units/{id}/holders/history retornando lista versionada de relacionamentos unit-holder com timestamps) e GEOWEB (componente de timeline de titulares com visualização cronológica e detalhes de cada período), garantindo rastreabilidade com RF-094 (Histórico de Titularidade), onde histórico é preservado através de soft delete de vínculos ao invés de remoção física, incluindo indicadores visuais de titular atual versus históricos e capacidade de filtrar por períodos de tempo específicos.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
