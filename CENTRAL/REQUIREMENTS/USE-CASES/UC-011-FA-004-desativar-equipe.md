---
modules: [GEOWEB]
epic: teams
---

# UC-011-FA-004: Desativar Equipe

Fluxo alternativo do UC-011 Gerenciar Equipes Técnicas desviando no passo 2 onde na listagem de equipes usuário clica menu de ações (três pontos) em equipe específica e seleciona opção Desativar Equipe disparando confirmação, sistema exibe modal amarelo warning com título "Desativar Equipe?" mensagem "A equipe Zona Norte será arquivada. Membros não perderão acesso aos dados mas equipe não aparecerá em listagens ativas. Histórico de atividades será preservado. Esta ação pode ser revertida" esclarecendo que é soft delete reversível não destrutivo, usuário confirma executando UPDATE teams SET status='INACTIVE' deactivated_by=$user_id deactivated_at=NOW() WHERE id=$id mantendo todos dados intactos apenas mudando flag, sistema não remove membros mantendo registros em team_members preservando histórico de quem participou quando joined_at, não remove comunidades atribuídas mantendo team_communities para auditoria de responsabilidades passadas, não deleta atividades vinculadas preservando rastreabilidade completa de unidades cadastradas aprovações realizadas relatórios gerados pela equipe, equipe desaparece de listagem padrão aplicando filtro WHERE status='ACTIVE' mas permanece acessível em aba Arquivadas ou filtro Mostrar Inativas permitindo consulta histórica, badge status muda para Inativo cinza identificando visualmente estado, registra auditoria detalhada em audit_log com action=TEAM_DEACTIVATED team_id reason opcional permitindo justificar desativação como "Projeto concluído", "Reorganização departamental", "Equipe mesclada com Zona Sul", pode ser reativada posteriormente via menu ações opção Reativar Equipe executando UPDATE status='ACTIVE' reactivated_by reactivated_at voltando a listagem normal.

**Ponto de Desvio:** Passo 2 do UC-011 (ação desativar na listagem)

**Retorno:** Equipe arquivada, histórico preservado, pode ser reativada

---

**Última atualização:** 2025-12-30
