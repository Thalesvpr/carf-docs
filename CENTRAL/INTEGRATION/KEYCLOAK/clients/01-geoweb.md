# Client GEOWEB

Portal web React para analistas REURB configurado como public client usando Authorization Code flow com PKCE obrigatório (code_challenge_method S256) garantindo segurança mesmo sem client_secret exposto no código frontend.

Redirect URIs incluem http://localhost:5173/* para desenvolvimento com Vite e https://geoweb.carf.example.com/* para produção com wildcard permitindo qualquer path. Web Origins configurado como "+" para herdar automaticamente de redirect URIs permitindo CORS apenas de origens autorizadas.

Scopes configurados: openid (obrigatório OIDC), profile (nome, username), email, roles (realm e client roles), carf-tenant (custom scope com mappers tenant_id e allowed_tenants). Frontend usa @react-keycloak/web para integração com Keycloak JS adapter.

Fluxo típico: usuário acessa GEOWEB sem token, Keycloak adapter detecta e redireciona para login com PKCE, usuário autentica, callback retorna para GEOWEB com tokens, adapter armazena access_token em memória e refresh_token em cookie httpOnly, todas requisições para GEOAPI incluem Authorization Bearer header.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
