---
modules: [GEOWEB]
epic: teams
---

# UC-011-FE-003: Tentativa de Remover Líder como Membro

Fluxo de exceção do UC-011 Gerenciar Equipes Técnicas desviando no FA-003 passo 4 quando usuário tenta remover membro mas sistema detecta que user_id selecionado para remoção é igual a team.leader_id indicando tentativa de remover líder, violando RN-006 que exige líder sempre ser membro da equipe mantendo accountability organizacional, sistema bloqueia operação antes de executar DELETE exibindo modal vermelho erro com título "Operação Não Permitida" mensagem "Não é possível remover o líder da equipe. Para remover este usuário: (1) Primeiro altere o líder da equipe para outro membro, (2) Depois remova o usuário como membro" orientando sobre sequência correta de ações, inclui botão Alterar Líder Agora que fecha modal de erro e abre diretamente modal de alteração de líder (FA-002) permitindo workflow contínuo sem navegar manualmente, usuário seleciona novo líder da lista de membros confirma alteração executando UPDATE teams SET leader_id = $new_leader, agora pode retornar para lista de membros e clicar remover no usuário que antes era líder mas agora é membro regular, sistema valida verificando user_id != leader_id condição agora satisfeita permite DELETE FROM team_members completando remoção com sucesso, alternativamente usuário pode clicar Cancelar aceitando que líder permanecerá na equipe e desistindo de remoção, regra garante toda equipe sempre tem líder identificável responsável por coordenação impedindo equipes órfãs sem accountability claro que causariam problemas de governança e rastreabilidade em processos de regularização fundiária com responsabilidades legais definidas.

**Ponto de Desvio:** FA-003 passo 4 (validação ao tentar remover)

**Retorno:** Remoção bloqueada, usuário altera líder primeiro ou cancela

---

**Última atualização:** 2025-12-30
