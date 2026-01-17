---
modules: [GEOAPI, REURBCAD]
epic: compatibility
---

# US-024: Ver Timeline de Alterações

Como analista, quero ver histórico de todas as alterações na unidade para que eu rastreie mudanças, onde o sistema mantém registro completo e imutável de todas as operações realizadas em cada unidade incluindo criação, modificações e exclusões, garantindo rastreabilidade completa e capacidade de auditoria para fins de conformidade e resolução de conflitos. O cenário principal de uso ocorre quando um analista acessa detalhes de uma unidade e visualiza seção dedicada ao histórico apresentando timeline cronológica de eventos, permitindo entender evolução do cadastro ao longo do tempo incluindo quem fez cada alteração, quando foi realizada, e quais valores foram modificados. Os critérios de aceitação incluem exibição de audit log completo contendo para cada entrada informações de quem executou a ação (usuário), quando ocorreu (timestamp preciso), e o que foi feito (tipo de operação e campos afetados), apresentação de diff de valores mostrando comparação lado a lado de antes/depois para cada campo modificado facilitando identificação exata das mudanças realizadas, ordenação cronológica reversa onde eventos mais recentes aparecem primeiro permitindo rápida visualização do histórico recente, e capacidade de filtrar timeline por tipo de operação (CREATE, UPDATE, DELETE) ou período de tempo para focar em eventos específicos de interesse. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/units/{id}/audit-log retornando lista paginada de eventos de auditoria com detalhes completos de cada modificação) e GEOWEB (componente de timeline com apresentação visual de eventos, diff destacado com cores, e controles de filtro), garantindo rastreabilidade com RF-060 (Auditoria de Alterações) e UC-002 (Caso de Uso de Workflow de Aprovação), onde eventos de audit log são imutáveis uma vez registrados, incluem contexto adicional como IP de origem e user agent, e são preservados mesmo quando unidade é excluída garantindo trilha de auditoria permanente.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
