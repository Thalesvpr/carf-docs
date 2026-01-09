---
modules: [GEOAPI, REURBCAD]
epic: security
---

# RF-006: 5 Níveis de Acesso (Roles)

Sistema deve suportar cinco níveis hierárquicos de acesso baseados em roles sendo SUPER_ADMIN com privilégios globais irrestritos ADMIN com gestão completa de tenant específico MANAGER com capacidade de aprovação de workflows ANALYST com permissões de cadastro e edição de dados FIELD_AGENT focado em coleta de dados em campo, roles devem ser definidos e gerenciados no Keycloak como realm roles ou client roles permitindo atribuição granular por usuário onde cada role possui conjunto específico de permissões mapeadas para operações de sistema, mapeamento de roles para permissões implementado no backend GEOAPI utilizando anotações ou decorators que verificam presence de role específica em claim roles do JWT antes de permitir execução de operação, controle de acesso baseado em role (RBAC - Role-Based Access Control) aplicado em toda plataforma incluindo módulos GEOAPI GEOWEB REURBCAD garantindo que usuário só visualize e execute funcionalidades permitidas para seu nível de acesso prevenindo escalação de privilégios e acesso não autorizado.

---

**Última atualização:** 2025-12-30
