---
modules: [GEOWEB]
epic: security
---

# RF-030: Filtrar Comunidades por Equipe

Usuários regulares (não ADMIN) visualizam apenas comunidades atribuídas à sua equipe onde filtro automático por equipe aplicado transparentemente em todas queries de listagem de comunidades adicionando cláusula WHERE community_id IN (SELECT community_id FROM team_communities WHERE team_id IN :user_teams), usuários com role ADMIN visualizam todas comunidades do tenant independente de vinculação a equipes permitindo gestão global e reatribuição de comunidades entre equipes conforme necessidades operacionais, visualização restrita para outros roles (MANAGER ANALYST FIELD_AGENT) implementa Row Level Security baseado em equipe garantindo segregação de dados e responsabilidades onde usuário só acessa informações relevantes para seu escopo de trabalho reduzindo complexidade de interface e prevenindo acesso não autorizado, implementação em módulos GEOWEB e GEOAPI com filtros aplicados automaticamente em camada de serviço ou ORM sem necessidade de lógica condicional em cada controller mantendo consistência e simplificando manutenção de código.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
