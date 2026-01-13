---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-036: Solicitar Alterações

Como gestor, quero solicitar alterações em unidade para que analista corrija sem rejeitar, onde o sistema oferece opção intermediária entre aprovação e rejeição permitindo que gestores solicitem ajustes específicos sem desaprovar completamente o trabalho, garantindo feedback construtivo e colaboração eficiente entre gestores e analistas. O cenário principal de uso ocorre quando gestor revisa unidade e identifica necessidade de ajustes menores que não justificam rejeição completa, permitindo selecionar ação de "Solicitar Alterações" e listar especificamente quais campos ou aspectos precisam ser corrigidos ou complementados. Os critérios de aceitação incluem capacidade de fornecer lista estruturada de alterações solicitadas onde gestor especifica item por item o que precisa ser ajustado com descrição clara de cada pendência, mudança automática de status para CHANGES_REQUESTED diferenciando de rejeição completa e indicando que são necessários apenas ajustes pontuais, apresentação clara para analista da lista de pendências através de interface dedicada mostrando cada item solicitado com checkboxes para marcar como resolvido, e processo de resubmissão após correções onde analista marca pendências como resolvidas e reenvia unidade para nova revisão do gestor. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/units/{id}/request-changes com lista de alterações e transição de status) e GEOWEB (formulário de solicitação de alterações com lista editável e interface de resolução de pendências), garantindo rastreabilidade com RF-059 (Solicitação de Alterações) e UC-002 (Caso de Uso de Workflow de Aprovação), onde cada alteração solicitada é rastreada individualmente permitindo acompanhamento granular, notificações são enviadas quando pendências são adicionadas ou resolvidas, e histórico completo de solicitações e resoluções é preservado em audit log.

---

**Última atualização:** 2025-12-30