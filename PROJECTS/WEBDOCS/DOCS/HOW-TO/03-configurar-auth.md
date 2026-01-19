# Configurar Autenticação

Guia para configurar integração com Keycloak habilitando proteção da seção /dev/ e autenticação do CMS.

Obter credenciais do Keycloak com equipe de infraestrutura incluindo URL do realm CARF, client ID do client carf-webdocs, e URLs de redirect autorizadas para ambiente de desenvolvimento.

Configurar variáveis de ambiente em arquivo .env. Variável KEYCLOAK_URL define URL base do Keycloak incluindo realm (ex: auth.carf.example.com/realms/carf). Variável KEYCLOAK_CLIENT_ID define client ID (carf-webdocs). Variável PUBLIC_URL define URL do site para callbacks.

Testar fluxo de login acessando rota protegida /dev/ no navegador. Redirect para Keycloak indica configuração correta de URL. Login com credenciais de desenvolvedor. Retorno para site indica callback configurado.

Verificar role dev acessando página que requer role. Usuário sem role deve ver página 403. Usuário com role deve ver conteúdo normalmente. Se role não atribuída, solicitar ao admin do Keycloak.

Testar logout acessando /auth/logout. Redirect para Keycloak logout e retorno para home indica fluxo completo funcionando. Tentar acessar /dev/ após logout deve redirecionar para login.

Configurar CMS em admin/config.yml ajustando backend para usar OAuth via Keycloak ao invés de GitHub nativo. Redirect URI do admin deve estar na lista de URIs autorizadas do client no Keycloak.

Troubleshooting comum inclui erro de redirect_uri quando URL não está autorizada no Keycloak, erro de CORS quando origem não está em Web Origins do client, e loop de redirect quando cookies não são salvos (verificar HTTPS e SameSite).

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
