---
modules: [GEOWEB]
epic: teams
---

# UC-011-FA-002: Alterar Líder da Equipe

Fluxo alternativo do UC-011 Gerenciar Equipes Técnicas desviando no passo 10 onde na tela de detalhes da equipe tab Membros usuário clica botão Alterar Líder exibindo dropdown listando apenas membros atuais da equipe via query SELECT users.* FROM users JOIN team_members WHERE team_id = $id AND status='ACTIVE' garantindo novo líder já faz parte da equipe conhece contexto e responsabilidades, usuário seleciona novo líder candidato (ex: Coordenador que vinha atuando como substituto e agora será promovido oficialmente), sistema exibe modal de confirmação amarelo com mensagem "Deseja alterar o líder da equipe de João Silva para Maria Santos? João receberá notificação da mudança" solicitando confirmação explícita devido impacto organizacional, usuário confirma executando UPDATE teams SET leader_id = $new_leader_id updated_by=$user_id updated_at=NOW() WHERE id = $team_id, atualiza role do antigo líder em team_members para Coordenador ou Analista rebaixando responsabilidade mas mantendo na equipe, atualiza role do novo líder para Leader se necessário refletindo mudança, sistema envia notificação ao antigo líder via email e push com título "Mudança de Liderança" mensagem "Você não é mais líder da equipe Zona Norte. Maria Santos assumiu a liderança. Você continua como membro Coordenador" garantindo transparência, envia notificação ao novo líder "Você foi designado líder da equipe Zona Norte. Responsabilidades incluem coordenação de atividades aprovação de cadastros e gestão de membros" orientando sobre atribuições, registra auditoria detalhada em audit_log com action=LEADER_CHANGED old_leader_id new_leader_id timestamp.

**Ponto de Desvio:** Passo 10 do UC-011 (tela de detalhes, ação específica)

**Retorno:** Líder alterado, ambos usuários notificados

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
