---
modules: [GEOWEB, REURBCAD]
epic: teams
---

# UC-011-FE-002: Líder Inválido ou Inativo

Fluxo de exceção do UC-011 Gerenciar Equipes Técnicas ocorrendo no passo 7 durante validação quando sistema verifica líder selecionado executando query SELECT * FROM users WHERE id = $leader_id AND tenant_id = $tenant detectando usuário inativo (status='INACTIVE'), deletado (deleted_at NOT NULL), ou não existente (query retorna null), tipicamente causado por ADMIN selecionando usuário que foi desativado entre momento de carregar dropdown e submeter formulário (race condition em sistemas com múltiplos administradores simultâneos), ou tentativa de selecionar líder que saiu da organização teve conta removida, sistema detecta invalidade verificando user.status !== 'ACTIVE' ou user === null, exibe modal vermelho erro com título "Líder Inválido" mensagem "O usuário selecionado está inativo ou foi removido. Selecione um usuário ativo como líder da equipe" esclarecendo problema, mantém formulário aberto recarrega dropdown de líderes executando query atualizada WHERE status='ACTIVE' removendo usuários inativos que podem ter sido desativados recentemente garantindo lista sempre sincronizada, campo Líder da Equipe resetado para estado vazio forçando nova seleção, usuário escolhe outro líder ativo da lista atualizada clica Criar Equipe validação agora passa prosseguindo normalmente, alternativamente se líder foi desativado por engano ADMIN pode navegar para menu Usuários reativar usuário específico alterando status para ACTIVE e retornar para criação de equipe agora com líder disponível no dropdown permitindo seleção válida.

**Ponto de Desvio:** Passo 7 do UC-011 (validação de líder)

**Retorno:** Criação bloqueada, usuário seleciona líder ativo e retenta

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
