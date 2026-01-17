---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-008: Visualizar Perfil

Como usuário autenticado, quero visualizar meu perfil e permissões para que eu saiba quais acessos tenho, onde a página de perfil apresenta de forma clara e organizada todas as informações relevantes sobre a conta do usuário e suas autorizações no sistema, garantindo transparência sobre capacidades e limitações do acesso. O cenário principal de uso ocorre quando o usuário acessa o menu de perfil através do header da aplicação e visualiza uma página dedicada contendo suas informações pessoais e de autorização, permitindo que ele compreenda rapidamente seu contexto de acesso incluindo seu role, tenant, e histórico de atividade recente. Os critérios de aceitação incluem a exibição completa de dados básicos como nome completo, endereço de email e role atual (SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_AGENT ou VIEWER), a indicação clara do tenant atual ao qual o usuário está associado e está operando no momento, a listagem de todas as permissões específicas que o role concede incluindo acesso a módulos e operações, e a exibição do timestamp do último login bem-sucedido para que o usuário possa identificar acessos não autorizados. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/accounts/me que retorna perfil completo do usuário autenticado extraído do token JWT) e GEOWEB (página de perfil com layout responsivo e componentes de exibição de dados), garantindo rastreabilidade com RF-033 (Visualização de Perfil), onde as informações são obtidas diretamente do sistema de autenticação e refletem o estado atual e real das permissões, incluindo atualização automática se roles ou permissões forem modificadas por administradores.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
