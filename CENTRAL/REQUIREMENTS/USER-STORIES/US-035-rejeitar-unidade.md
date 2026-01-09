---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# US-035: Rejeitar Unidade

Como gestor, quero rejeitar unidade com motivo para que analista corrija, onde o sistema permite que gestores identifiquem problemas em unidades cadastradas e as devolvam para correção com justificativa clara, garantindo qualidade dos dados através de ciclo de revisão e correção estruturado. O cenário principal de uso ocorre quando gestor revisa unidade e identifica problemas que impedem aprovação como dados incompletos ou incorretos, permitindo selecionar ação de rejeição e fornecer motivo detalhado explicando o que precisa ser corrigido para que analista possa realizar ajustes apropriados. Os critérios de aceitação incluem exigência de campo "motivo" obrigatório onde gestor deve fornecer texto explicativo detalhando razões da rejeição e orientações para correção, mudança automática de status para REJECTED indicando que unidade foi revisada e necessita correções, envio de notificação com motivo ao criador da unidade incluindo texto completo da justificativa da rejeição e orientações para resubmissão, e capacidade de analista resubmeter unidade para aprovação após realizar correções solicitadas reiniciando ciclo de workflow. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/units/{id}/reject com validação de motivo obrigatório e transição de status) e GEOWEB (botão de rejeição com formulário para motivo e notificações), garantindo rastreabilidade com RF-058 (Rejeição de Unidades) e UC-002 (Caso de Uso de Workflow de Aprovação), onde rejeições são registradas em audit log com motivo completo, notificações incluem link direto para edição, e histórico de rejeições/resubmissões é preservado mostrando iterações até aprovação final.

---

**Última atualização:** 2025-12-30