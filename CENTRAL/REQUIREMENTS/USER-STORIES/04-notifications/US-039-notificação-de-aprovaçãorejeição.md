---
modules: [REURBCAD]
epic: compatibility
---

# US-039: Notificação de Aprovação/Rejeição

Como analista, quero receber notificação quando unidade for aprovada/rejeitada para que eu saiba resultado, onde o sistema envia alertas automáticos mantendo criador de unidade informado sobre decisões de workflow sem necessidade de verificação manual constante, garantindo comunicação eficiente e resposta rápida a ações necessárias. O cenário principal de uso ocorre automaticamente quando gestor executa ação de aprovação ou rejeição em unidade, onde sistema identifica criador original e envia notificação através de canais configurados informando sobre decisão tomada e incluindo contexto relevante para ação subsequente. Os critérios de aceitação incluem envio de notificação in-app apresentada em central de notificações dentro da aplicação com badge indicando quantidade de notificações não lidas e lista cronológica de alertas recebidos, opção de recebimento por email configurável nas preferências do usuário permitindo ativar/desativar envio de emails para notificações de workflow, e inclusão de link direto para unidade em questão permitindo navegação com um clique desde notificação até página de detalhes da unidade para visualização ou edição conforme necessário. Esta funcionalidade é implementada pelos módulos GEOAPI (sistema de notificações acionado por eventos de aprovação/rejeição com templates de mensagem e integração com serviço de email) e GEOWEB (componente de central de notificações no header e gerenciamento de preferências), garantindo rastreabilidade com UC-002 (Caso de Uso de Workflow de Aprovação), onde notificações incluem informações contextuais como nome da unidade e motivo em caso de rejeição, usuários podem marcar notificações como lidas, e histórico completo de notificações é mantido permitindo consulta posterior de alertas antigos.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
