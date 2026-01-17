---
modules: [GEOWEB, REURBCAD]
epic: security
---

# UC-011: Gerenciar Equipes Técnicas

Caso de uso permitindo usuários autorizados (ADMIN com permissão teams.create para gerenciar equipes de todo tenant sem restrições, MANAGER com teams.manage para gerenciar equipes do seu escopo organizacional) criarem e gerenciarem equipes técnicas de trabalho organizando colaboradores em grupos funcionais definindo líderes responsáveis atribuindo comunidades específicas para cada equipe otimizando distribuição de carga de trabalho coordenação de atividades de campo rastreamento de desempenho e accountability em processos de regularização fundiária urbana após autenticação e disponibilidade de usuários cadastrados no tenant, onde fluxo principal inicia com acesso ao menu Administração submenu Equipes exibindo tela de gerenciamento listando todas equipes existentes do tenant em grid paginado com colunas mostrando Nome da Equipe (ex: "Equipe Zona Norte", "Levantamento Vila Nova"), Líder da Equipe exibindo nome completo do usuário designado como responsável, Número de Membros contando total de team_members ativos via COUNT agregado, Comunidades Atribuídas listando nomes separados por vírgula ou badge numérico "5 comunidades" clicável para detalhes, Status badge colorido mostrando Ativa em verde ou Inativa em cinza, ações editar visualizar desativar via ícones, usuário clica botão + Nova Equipe no canto superior direito abrindo formulário modal de criação exibindo campos obrigatórios e opcionais incluindo input text Nome da Equipe aceitando string descritiva única identificando equipe (validação unique constraint por tenant), textarea Descrição opcional permitindo detalhar escopo responsabilidades ou área geográfica da equipe (ex: "Responsável por levantamentos na região norte incluindo bairros X Y Z"), dropdown Líder da Equipe listando todos usuários ativos do tenant via query SELECT * FROM users WHERE tenant_id = $tenant AND status = 'ACTIVE' ORDER BY name filtrando roles apropriados (MANAGER ANALYST FIELD_AGENT excluindo ADMIN típico), radio buttons Status selecionando Ativa (equipe operacional participando de workflow) ou Inativa (equipe arquivada por reorganização finalização de projeto ou saída de membros), usuário preenche dados básicos informando nome descritivo selecionando líder marcando status Ativa e clica Criar Equipe disparando validação verificando nome não vazio trim() !== '', nome único comparando com existing teams WHERE name = $name AND tenant_id = $tenant retornando count = 0, líder selecionado existe na tabela users e possui status ACTIVE garantindo referência válida, se validação passa sistema cria registro em tabela teams inserindo tenant_id name description leader_id status=ACTIVE created_by=user_id created_at=NOW() retornando team_id gerado, redireciona automaticamente para tela de detalhes da equipe renderizando layout completo com tabs mostrando Membros Comunidades Atividades Métricas, tab Membros exibe lista vazia inicialmente com mensagem "Nenhum membro adicionado" e botão + Adicionar Membro, usuário clica abrindo modal de seleção exibindo grid de usuários disponíveis do tenant com checkboxes permitindo seleção múltipla mostrando nome email role foto, filtros por role departamento status facilitando busca em tenants grandes com centenas de usuários, usuário marca checkboxes de 5-10 usuários desejados seleciona dropdown Papel do Membro para cada um oferecendo Coordenador (substituto do líder auxilia coordenação), Analista (responsável por análises técnicas aprovações validações), Agente de Campo (executa levantamentos coleta dados mobile), clica Adicionar executando validação verificando usuários selecionados não duplicados comparando user_ids com members já adicionados, usuários estão ativos validando status=ACTIVE de cada um, se validação passa sistema insere registros em team_members table criando row por usuário com team_id user_id role joined_at=NOW(), atualiza contador de membros na UI exibindo lista completa com cards mostrando foto nome role e ação remover, tab Comunidades permite atribuir responsabilidade geográfica clicando + Atribuir Comunidade abrindo modal listando todas communities do tenant com checkboxes, usuário marca 3-5 comunidades adjacentes geograficamente próximas ou tematicamente relacionadas (ex: todas comunidades de interesse social REURB-S) clica Atribuir criando vínculos em team_communities table inserindo team_id community_id assigned_at=NOW(), sistema exibe toast verde "Equipe criada com sucesso. 8 membros e 5 comunidades atribuídas" confirmando operação, equipe aparece em listagem principal com informações atualizadas refletindo configuração completa, líder designado recebe notificação email e push informando "Você foi designado líder da equipe Zona Norte" com link para acessar detalhes, membros adicionados recebem notificação "Você foi adicionado à equipe Zona Norte" orientando sobre nova atribuição, sistema registra todas operações em audit_log table com action=TEAM_CREATED actor=ADMIN timestamp details JSON contendo team_id name members_count para rastreabilidade e compliance. Fluxos alternativos incluem editar equipe existente modificando nome descrição status (UC-011-FA-001), alterar líder da equipe transferindo responsabilidade com notificações (UC-011-FA-002), remover membro da equipe com validação impedindo remover líder (UC-011-FA-003), e desativar equipe arquivando sem perder histórico (UC-011-FA-004). Fluxos de exceção cobrem nome de equipe duplicado impedindo criação (UC-011-FE-001), líder inválido ou inativo rejeitando seleção (UC-011-FE-002), tentativa de remover líder como membro bloqueando operação (UC-011-FE-003), equipe sem membros permitindo com warning (UC-011-FE-004), e usuário já pertencendo a outra equipe oferecendo mover ou adicionar em ambas (UC-011-FE-005).

**Fluxos Alternativos:**
- UC-011-FA-001: Editar equipe existente
- UC-011-FA-002: Alterar líder da equipe

**Fluxos de Exceção:**
- UC-011-FE-001: Nome de equipe duplicado
- UC-011-FE-002: Líder inválido ou inativo

**Regras de Negócio:**
- RN-001: Nome da equipe deve ser único dentro do tenant validado via constraint UNIQUE
- RN-002: Equipe deve ter pelo menos um líder definido obrigatoriamente
- RN-003: Líder da equipe deve ser membro ativo validando status=ACTIVE
- RN-004: Usuários podem pertencer a múltiplas equipes simultaneamente sem restrição
- RN-005: Apenas ADMIN e MANAGER podem criar editar ou desativar equipes (ANALYST readonly)
- RN-006: Líder da equipe não pode ser removido como membro (alterar líder primeiro via FA-002)
- RN-007: Equipes inativas mantêm histórico completo mas não aparecem em listagens padrão (filtro WHERE status='ACTIVE')
- RN-008: Comunidades podem estar atribuídas a múltiplas equipes permitindo redundância
- RN-009: Desativar equipe não remove membros nem histórico preservando auditoria
- RN-010: Todas operações em equipes são auditadas em audit_log para compliance

**Rastreabilidade:**
- RF-024, RF-026, RF-050
- US-030

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
