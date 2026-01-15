---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-080: Aprovar ou Rejeitar Processo

Como gestor com autoridade de aprovação, quero analisar e decidir aprovar ou rejeitar processos de legitimação submetidos para que titulação avance apenas para casos adequadamente instruídos ou retorne para correção quando necessário, onde a funcionalidade deve fornecer botões claros de "Aprovar" e "Rejeitar" para processos em status PENDING_APPROVAL, garantindo exigência de motivo textual obrigatório caso processo seja rejeitado para justificar decisão, permitindo que status seja atualizado automaticamente para APPROVED ou REJECTED conforme decisão e notificação seja enviada ao analista responsável informando resultado. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de aprovação consumindo GEOAPI através dos endpoints POST /api/legitimation/processes/{id}/approve e POST /api/legitimation/processes/{id}/reject que processam decisão e atualizam workflow, integrada ao RF-174 (Aprovação de Processos) e UC-009 (Gestão de Processos de Legitimação). Os critérios de aceitação incluem disponibilidade de botões "Aprovar" e "Rejeitar" visíveis apenas para usuários com perfil de gestor em processos PENDING_APPROVAL, click em "Aprovar" solicitando confirmação e executando aprovação imediata sem campos adicionais, click em "Rejeitar" abrindo modal ou formulário solicitando motivo textual obrigatório da rejeição, validação impedindo rejeição sem motivo preenchido com mensagem clara ao gestor, atualização automática de status do processo para APPROVED ao aprovar ou REJECTED ao rejeitar, registro de timestamp de decisão (approved_at ou rejected_at) e usuário aprovador/rejeitador no histórico, armazenamento de motivo de rejeição associado ao processo quando aplicável, envio de notificação por email e/ou in-app para analista responsável informando decisão tomada, inclusão de motivo de rejeição na notificação quando processo for rejeitado orientando correções necessárias, e possibilidade de processo rejeitado retornar para status DRAFT permitindo correção e resubmissão pelo analista. A rastreabilidade conecta esta user story ao RF-174 (Decisão sobre Processos) UC-009 (Gestão de Legitimação) e endpoints POST /api/legitimation/processes/{id}/approve e reject, garantindo governança adequada e rastreabilidade completa de decisões sobre processos de titulação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
