---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: teams
---

# UC-011-FA-003: Remover Membro da Equipe

Fluxo alternativo do UC-011 Gerenciar Equipes Técnicas desviando no passo 10 onde na lista de membros da equipe usuário clica ícone remover (X vermelho) ao lado de membro específico disparando confirmação, sistema exibe modal amarelo warning perguntando "Deseja remover Carlos Oliveira da equipe Zona Norte? O usuário perderá acesso específico desta equipe mas manterá acesso geral ao sistema" esclarecendo impacto, usuário confirma sistema valida se membro não é o líder verificando user_id != team.leader_id pois líder não pode ser removido diretamente (RN-006 exige alterar líder primeiro via FA-002), se validação passa executa DELETE FROM team_members WHERE team_id = $id AND user_id = $user_id removendo vínculo, atualiza contador de membros decrementando total exibido, envia notificação ao usuário removido via email informando "Você foi removido da equipe Zona Norte" garantindo transparência sobre mudanças organizacionais, registra auditoria em audit_log com action=MEMBER_REMOVED removed_user_id team_id timestamp, lista de membros atualiza removendo card do usuário exibindo toast "Membro removido com sucesso", permite adicionar novamente posteriormente se necessário via + Adicionar Membro reintegrando usuário sem restrições.

**Ponto de Desvio:** Passo 10 do UC-011 (ação remover membro)

**Retorno:** Membro removido, notificação enviada, lista atualizada

---

**Última atualização:** 2025-12-30
