---
modules: [GEOWEB]
epic: usability
---

# UC-011-FE-005: Usuário Já Pertence a Outra Equipe

Fluxo de exceção do UC-011 Gerenciar Equipes Técnicas ocorrendo no passo 11 durante validação ao adicionar membros quando sistema detecta que usuário selecionado já pertence a outra equipe ativa verificando query SELECT team_id FROM team_members WHERE user_id = $user AND team_id IN (SELECT id FROM teams WHERE status='ACTIVE') retornando team_id não null indicando vínculo existente, exibe modal amarelo warning com ícone de informação título "Usuário Já em Equipe" mensagem "Carlos Oliveira já pertence à equipe Zona Sul. O que deseja fazer?" oferecendo três opções via radio buttons: Mover para Esta Equipe removendo de equipe anterior e adicionando na atual garantindo usuário pertence apenas a uma equipe por vez (modelo exclusivo simplificado), Adicionar em Ambas permitindo múltiplas equipes simultaneamente conforme RN-004 útil para coordenadores que atuam em múltiplos projetos ou especialistas compartilhados entre equipes (modelo mais flexível complexo), ou Cancelar desistindo de adicionar mantendo usuário apenas na equipe original, se usuário escolhe Mover executa transação BEGIN DELETE FROM team_members WHERE user_id=$user INSERT INTO team_members VALUES ($new_team, $user, $role) COMMIT garantindo atomicidade envia notificação ao usuário "Você foi transferido da equipe Zona Sul para Zona Norte" e ao líder da equipe anterior "Carlos Oliveira foi removido da sua equipe (transferido)", se escolhe Adicionar em Ambas simplesmente executa INSERT sem DELETE criando segundo vínculo permite usuário ver atividades de múltiplas equipes no dashboard com filtro seletor de contexto complicando UX mas aumentando flexibilidade organizacional, sistema registra escolha em audit_log com action=MEMBER_MOVED ou MEMBER_ADDED_MULTIPLE from_team_id to_team_id rastreando mobilidade interna de colaboradores entre estruturas organizacionais útil para análise de recursos humanos e otimização de alocação de equipe.

**Ponto de Desvio:** Passo 11 do UC-011 (validação ao adicionar membro)

**Retorno:** Escolha oferecida, usuário decide mover adicionar ambas ou cancelar

---

**Última atualização:** 2025-12-30
