---
modules: [GEOWEB, REURBCAD]
epic: teams
---

# UC-011-FE-004: Equipe sem Membros

Fluxo de exceção do UC-011 Gerenciar Equipes Técnicas ocorrendo no passo 10 quando usuário cria equipe define líder mas não adiciona nenhum membro via + Adicionar Membro deixando team_members vazio exceto líder que tecnicamente também é membro mas pode não estar explicitamente adicionado dependendo de implementação, ao tentar finalizar ou navegar para outra tela sistema detecta COUNT team_members = 0 indicando equipe sem membros operacionais além de líder, exibe modal amarelo warning com ícone de informação título "Equipe sem Membros" mensagem "A equipe foi criada mas não possui membros adicionados. Uma equipe sem membros não poderá executar atividades de campo ou cadastro. Deseja continuar mesmo assim?" oferecendo escolha explícita, usuário decide entre Continuar aceitando limitação permitindo criar equipe skeleton que será populada posteriormente conforme contratação de novos colaboradores ou transferência de membros de outras equipes executando criação normalmente marcando flag incomplete=true ou similar para identificar equipes não totalmente configuradas, ou Adicionar Membros Agora mantendo modal de criação aberto e automaticamente abrindo modal de seleção de membros (passo 10) permitindo adicionar usuários imediatamente completando configuração antes de finalizar, se continuar sem membros equipe aparece na listagem com badge laranja "Incompleta" ou "Sem Membros" alertando visualmente MANAGER sobre necessidade de configuração adicional, dashboard de métricas pode incluir widget "Equipes Incompletas" listando teams sem membros facilitando identificação e ação corretiva, equipe funciona normalmente para fins de estrutura organizacional mas não pode ter unidades ou atividades atribuídas até adicionar ao menos um membro operacional garantindo sempre há pessoa responsável por executar trabalho atribuído.

**Ponto de Desvio:** Passo 10 do UC-011 (tentativa de finalizar sem membros)

**Retorno:** Warning exibido, usuário adiciona membros ou continua com equipe incompleta

---

**Última atualização:** 2025-12-30
