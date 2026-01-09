---
modules: [GEOAPI, GEOWEB]
epic: security
---

# RF-008: ADMIN - Gestão de Tenant

Usuários com role ADMIN podem gerenciar todos recursos dentro do seu tenant específico onde podem criar novos usuários no tenant atribuindo roles apropriadas (MANAGER ANALYST FIELD_AGENT) e configurando permissões iniciais, capacidade de gerenciar comunidades incluindo criação edição desativação configuração de geometrias atribuição de equipes e definição de parâmetros específicos de cada comunidade dentro do tenant, restrição de acesso a outros tenants implementada através de filtro automático Row Level Security (RLS) aplicado em todas queries de banco de dados garantindo que ADMIN visualize e manipule apenas dados onde tenant_id corresponde ao tenant do próprio usuário conforme claim tenant_id presente no JWT, implementação em módulos GEOWEB e GEOAPI com interface administrativa que exibe funcionalidades completas de gestão de tenant incluindo dashboards gerenciais listagens de usuários e comunidades configurações de tenant e relatórios operacionais.

---

**Última atualização:** 2025-12-30
