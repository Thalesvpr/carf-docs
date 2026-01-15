---
modules: [GEOAPI, GEOWEB]
epic: security
---

# RF-014: Logout e Revogação de Token

Usuário deve poder fazer logout voluntário do sistema revogando tokens ativos onde botão de logout fica visível em interface de usuário tipicamente em menu de perfil ou barra de navegação principal permitindo acesso fácil e intuitivo, processo de logout remove tokens (access_token refresh_token) do storage local do cliente (sessionStorage localStorage cookies) prevenindo reutilização após logout e garantindo que sessão seja efetivamente encerrada, redirecionamento automático para tela de login ocorre imediatamente após logout onde usuário vê mensagem de confirmação "Logout realizado com sucesso" e é apresentado novamente com formulário de autenticação caso deseje acessar sistema novamente, implementação em módulos GEOWEB e REURBCAD inclui chamada opcional para endpoint de revogação do Keycloak /protocol/openid-connect/logout para invalidar tokens no servidor prevenindo que tokens ainda válidos sejam utilizados por atacantes que eventualmente obtiveram cópia antes do logout.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
