---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-001: Login com OAuth2

Como usuário do sistema, quero fazer login via OAuth2 com Keycloak para que eu possa acessar o sistema de forma segura, onde o fluxo de autenticação implementa o padrão OAuth2 Authorization Code Flow com PKCE (Proof Key for Code Exchange), garantindo proteção contra ataques de interceptação de código de autorização. O cenário principal de uso inicia quando o usuário acessa a tela de login e é redirecionado para o servidor Keycloak, onde insere suas credenciais (usuário e senha), permitindo que o sistema valide a autenticação e retorne um authorization code que é trocado por tokens JWT (access token e refresh token), os quais são armazenados de forma segura no navegador utilizando httpOnly cookies ou localStorage com criptografia. Os critérios de aceitação incluem o redirecionamento funcional para Keycloak, a implementação correta do Authorization Code com PKCE, o armazenamento seguro dos tokens JWT, o redirecionamento pós-login para a página apropriada do sistema, e o tratamento adequado de erros como credenciais inválidas ou falhas de comunicação com o servidor de autenticação. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoints POST /api/auth/login e POST /api/auth/refresh) e GEOWEB (componente de login e gerenciamento de sessão), garantindo rastreabilidade com RF-001 (Sistema de Autenticação OAuth2) e UC-001 (Caso de Uso de Autenticação), onde apenas usuários com credenciais válidas no Keycloak conseguem acessar o sistema, e falhas são registradas em logs para auditoria.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
