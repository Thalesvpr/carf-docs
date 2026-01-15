---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-034: Aprovar Unidade

Como gestor, quero aprovar unidade cadastrada para que ela passe para próxima etapa, onde o sistema implementa workflow de aprovação permitindo que gestores validem unidades cadastradas por analistas promovendo-as de rascunho para status aprovado, garantindo controle de qualidade e rastreabilidade das aprovações realizadas. O cenário principal de uso ocorre quando gestor revisa detalhes de unidade em status DRAFT e após validar que informações estão corretas e completas clica em botão "Aprovar", permitindo que sistema execute transição de status e registre aprovação no histórico da unidade. Os critérios de aceitação incluem visibilidade do botão "Aprovar" restrita a usuários com role MANAGER ou superior através de controle de acesso baseado em permissões, mudança automática de status de DRAFT para APPROVED quando aprovação é confirmada refletindo progressão no workflow, envio de notificação automática ao criador da unidade informando que seu cadastro foi aprovado com link para visualizar detalhes, e registro completo no audit log capturando quem aprovou, quando a aprovação ocorreu, e transição de status realizada para rastreabilidade e auditoria. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/units/{id}/approve com validações de permissão e transição de status) e GEOWEB (botão de aprovação visível condicionalmente e modal de confirmação), garantindo rastreabilidade com RF-057 (Aprovação de Unidades) e UC-002 (Caso de Uso de Workflow de Aprovação), onde aprovações são irreversíveis sem autorização superior e gatilham notificações para stakeholders relevantes, incluindo validações que asseguram completude de dados obrigatórios antes de permitir aprovação.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
