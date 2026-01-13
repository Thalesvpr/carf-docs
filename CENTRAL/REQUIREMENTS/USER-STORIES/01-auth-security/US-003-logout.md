---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-003: Logout

Como usuário autenticado, quero fazer logout do sistema para que minha sessão seja encerrada com segurança, onde o processo de logout executa uma limpeza completa de todos os tokens de autenticação (access token e refresh token) tanto no armazenamento local do navegador quanto na sessão do servidor Keycloak, garantindo que nenhum dado sensível permaneça acessível após o encerramento da sessão. O cenário principal de uso inicia quando o usuário clica no botão de logout na interface, permitindo que o sistema execute uma sequência ordenada de operações incluindo a revogação dos tokens no Keycloak, a remoção de todos os tokens do localStorage ou cookies, a limpeza de quaisquer dados em cache relacionados à sessão do usuário, e o redirecionamento final para a tela de login. Os critérios de aceitação incluem a remoção completa de tokens do storage local do navegador, a revogação efetiva da sessão no servidor Keycloak através de chamada ao endpoint de logout, o redirecionamento automático para a tela de login após logout bem-sucedido, e a garantia de que não há dados sensíveis (incluindo informações de perfil, permissões ou dados de negócio) permanecendo no browser após o logout. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/auth/logout que coordena com Keycloak) e GEOWEB (componente de logout e limpeza de estado da aplicação), garantindo rastreabilidade com RF-014 (Logout Seguro) e UC-001 (Caso de Uso de Autenticação), onde a segurança é priorizada através da limpeza completa de vestígios de autenticação e quaisquer tentativas de acesso subsequentes são bloqueadas até nova autenticação válida.

---

**Última atualização:** 2025-12-30