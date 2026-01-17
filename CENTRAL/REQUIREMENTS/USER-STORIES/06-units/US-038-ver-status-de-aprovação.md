---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-038: Ver Status de Aprovação

Como analista, quero ver status de aprovação de unidades para que eu saiba quais estão pendentes, onde o sistema apresenta de forma clara e visualmente distintiva o estado atual de cada unidade no workflow de aprovação, garantindo que usuários compreendam rapidamente situação de seus cadastros e possam priorizar ações necessárias. O cenário principal de uso ocorre em visualizações de listagem e detalhes de unidades onde status é exibido através de badges coloridos e textos descritivos, permitindo identificação imediata do estágio de aprovação e necessidade de ação por parte do usuário. Os critérios de aceitação incluem apresentação de badge visual com status usando cores distintas para DRAFT (cinza ou amarelo indicando rascunho), APPROVED (verde indicando aprovado e pronto), REJECTED (vermelho indicando rejeitado necessitando correções) e CHANGES_REQUESTED (laranja indicando ajustes solicitados), capacidade de filtrar listagem por status permitindo visualizar apenas unidades em estágio específico como todas as DRAFT pendentes de submissão ou REJECTED necessitando correção, e exibição de contador de pendentes mostrando quantitativamente quantidade de unidades em cada status facilitando priorização de trabalho. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/units?status=DRAFT suportando filtro por status e agregações para contadores) e GEOWEB (componentes de badge estilizados, filtros de status e dashboard com contadores), garantindo rastreabilidade com RF-056 (Visualização de Status de Aprovação) e UC-002 (Caso de Uso de Workflow de Aprovação), onde status reflete estado real em tempo real, badges são consistentes em toda aplicação, e tooltips fornecem informações adicionais como data da última transição de status e usuário responsável.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
