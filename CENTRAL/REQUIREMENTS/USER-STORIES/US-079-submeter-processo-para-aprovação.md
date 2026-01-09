---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-079: Submeter Processo para Aprovação

Como analista responsável por processo de legitimação, quero submeter processo completo com todos documentos anexados para aprovação formal do gestor para que titulação avance para próxima etapa do workflow, onde a funcionalidade deve executar validação de completude verificando presença de documentos obrigatórios antes de permitir submissão, garantindo mudança automática de status do processo de DRAFT para PENDING_APPROVAL ao submeter, permitindo envio de notificação automática para gestor responsável informando que há processo aguardando análise. Esta funcionalidade é implementada pelo módulo GEOWEB com botão de submissão e validações consumindo GEOAPI através do endpoint POST /api/legitimation/processes/{id}/submit que valida e atualiza status, integrada ao RF-173 (Submissão de Processo) e UC-009 (Gestão de Processos de Legitimação). Os critérios de aceitação incluem disponibilidade de botão "Submeter para aprovação" visível apenas para processos em status DRAFT, validação prévia de completude verificando se todos documentos obrigatórios do checklist foram anexados, bloqueio de submissão com mensagem clara se validação falhar indicando documentos faltantes, confirmação de submissão solicitando que analista confirme ação antes de prosseguir, atualização automática de status do processo de DRAFT para PENDING_APPROVAL ao confirmar submissão, registro de timestamp de submissão (submitted_at) e usuário submetedor no histórico do processo, envio de notificação por email e/ou in-app para gestor responsável informando novo processo aguardando análise, inclusão de link direto para processo na notificação facilitando acesso imediato pelo gestor, bloqueio de edições no processo após submissão até que seja aprovado ou rejeitado retornando para DRAFT, e atualização visual da interface indicando novo status com badge ou cor diferenciada. A rastreabilidade conecta esta user story ao RF-173 (Workflow de Aprovação) UC-009 (Gestão de Legitimação) e endpoint POST /api/legitimation/processes/{id}/submit, garantindo controle adequado de qualidade antes de avanço no fluxo de titulação.

---

**Última atualização:** 2025-12-30
