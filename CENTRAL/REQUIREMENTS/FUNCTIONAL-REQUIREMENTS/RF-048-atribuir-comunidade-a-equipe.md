---
modules: [GEOWEB, REURBCAD]
epic: teams
---

# RF-048: Atribuir Comunidade a Equipe

Usuários com role ADMIN podem atribuir comunidades a equipes específicas onde múltiplas equipes podem ser vinculadas a mesma comunidade permitindo colaboração entre times ou distribuição de responsabilidades compartilhadas (ex: equipe de campo + equipe de análise documental), controle de visibilidade automático onde membros de equipes vinculadas visualizam comunidade em listagens e podem acessar unidades relacionadas respeitando permissões de role individual enquanto membros de equipes não vinculadas não visualizam comunidade exceto ADMIN que vê todas, filtros automáticos aplicados em queries de listagem conforme RF-030 adicionando join com tabela de associação team_communities garantindo que usuários regulares vejam apenas comunidades sob responsabilidade de suas equipes, implementação em módulos GEOWEB e GEOAPI com interface de gerenciamento de atribuições permitindo vincular/desvincular equipes via seleção múltipla ou drag-and-drop atualização imediata de visibilidade para usuários afetados e log de alterações registrando mudanças de atribuição para auditoria.

---

**Última atualização:** 2025-12-30
