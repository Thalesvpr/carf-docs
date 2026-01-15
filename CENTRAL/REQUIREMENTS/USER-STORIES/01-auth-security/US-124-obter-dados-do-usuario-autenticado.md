---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# US-124: Obter Dados do Usuario Autenticado

Como Usuario autenticado quero visualizar meus dados de perfil e permissoes para que possa saber quais roles e acessos possuo no sistema e entender meu nivel de autorizacao, onde o endpoint implementado em GEOAPI expoe a rota /api/auth/me retornando informacoes completas do usuario extraidas do token JWT ou sessao autenticada, garantindo que apenas usuarios autenticados possam acessar este endpoint retornando 401 Unauthorized para requisicoes sem token valido, permitindo que o frontend GEOWEB exiba nome email foto de perfil e lista de roles atribuidas ao usuario logado, incluindo informacoes de tenant para contextualizacao em ambientes multi-tenant onde cada usuario pertence a uma organizacao especifica, onde a resposta inclui objeto UserInfo com propriedades id username email fullName profilePictureUrl roles e tenantId, garantindo rastreabilidade ao requisito funcional RF-007 que especifica gerenciamento de perfil de usuario, permitindo que a interface do frontend adapte menus e funcionalidades disponiveis conforme as permissoes do usuario incluindo ocultacao de opcoes administrativas para usuarios com role Analyst, incluindo validacao de token JWT com verificacao de expiracao e assinatura HMAC garantindo que tokens adulterados ou expirados sejam rejeitados, onde a implementacao em GEOAPI utiliza middleware de autenticacao para extrair claims do token JWT incluindo sub claim para identificacao do usuario e roles claim para lista de perfis, permitindo atualizacao automatica das informacoes de perfil quando o token for renovado atraves do fluxo de refresh token, garantindo que mudancas de permissoes efetuadas por administradores sejam refletidas apos proximo login ou renovacao de token, incluindo testes unitarios que validam mapeamento correto entre claims JWT e modelo de dominio UserInfo, onde testes de integracao verificam fluxo completo de autenticacao OAuth2 seguido de chamada ao endpoint /api/auth/me para obter dados do usuario, garantindo compatibilidade com provedores OAuth2 externos incluindo Google Azure AD e servidores Keycloak internos, permitindo que aplicacoes mobile Android e iOS utilizem este endpoint para exibir drawer de navegacao personalizado com informacoes do usuario logado.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
