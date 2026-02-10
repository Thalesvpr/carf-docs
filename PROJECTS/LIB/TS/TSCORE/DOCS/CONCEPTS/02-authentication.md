---
type: leaf
status: review
updated: 2026-02-08
---

# Autenticacao

Sistema de autenticacao integrado com Keycloak usando OAuth2 Authorization Code com PKCE (Proof Key for Code Exchange). O KeycloakClient do @carf/tscore gerencia o ciclo de vida completo de tokens incluindo obtencao, refresh automatico, extracao de roles e verificacao de permissoes hierarquicas. O fluxo e identico para todos os clientes do ecossistema CARF (GEOWEB, REURBCAD, ADMIN) com diferenca apenas nos adapters de storage e navegacao documentados em [02a-authentication-config](./02a-authentication-config.md).

## Fluxo OAuth2 Authorization Code com PKCE

O fluxo inicia quando a aplicacao chama o metodo login do KeycloakClient. O cliente gera um code_verifier aleatorio criptograficamente seguro de 128 caracteres usando caracteres URL-safe (A-Z, a-z, 0-9, hifen, ponto, underline, til). A partir do code_verifier, deriva o code_challenge aplicando SHA-256 seguido de codificacao base64url sem padding. O code_verifier e armazenado no storage local para uso posterior, junto com um state aleatorio para prevencao de CSRF.

O cliente redireciona o navegador (ou browser do sistema no mobile) para o authorization endpoint do Keycloak com os parametros response_type code, client_id, redirect_uri, code_challenge, code_challenge_method S256, scope (openid profile, com offline_access adicional no mobile) e state. O usuario autentica no formulario do Keycloak com credenciais.

Apos autenticacao bem-sucedida, o Keycloak redireciona para o redirect_uri com dois query params: code (authorization code de uso unico) e state. A aplicacao intercepta este redirect via NavigationAdapter, valida que o state recebido corresponde ao armazenado (protecao contra CSRF) e chama handleCallback. O cliente envia POST para o token endpoint do Keycloak com grant_type authorization_code, code, redirect_uri, client_id e code_verifier original. O Keycloak verifica o hash SHA-256 do code_verifier contra o code_challenge enviado anteriormente e, se valido, retorna access_token (JWT de 5 minutos), refresh_token e id_token.

## Ciclo de Vida de Tokens

O access_token tem duracao de 5 minutos conforme configuracao do realm CARF. O metodo getToken verifica a expiracao do token antes de retorna-lo, considerando uma margem de seguranca de 5 minutos: se o token expira em menos de 5 minutos, o cliente executa refresh proativo sem aguardar expiracao efetiva. O refresh ocorre transparentemente sem intervencao do usuario, enviando o refresh_token ao token endpoint com grant_type refresh_token.

Em aplicacoes web (GEOWEB, ADMIN), o refresh_token expira com o SSO Session Idle de 30 minutos. Se o usuario ficar inativo por mais de 30 minutos, o refresh falha com 401 e o cliente emite o evento auth:session-expired para que a aplicacao redirecione para login. Em aplicacoes mobile (REURBCAD), o scope offline_access garante refresh_token de 30 dias, permitindo que agentes de campo mantenham sessao entre idas a campo sem re-autenticacao.

## Silent Refresh

O silent refresh e o mecanismo pelo qual o getToken renova automaticamente o access_token usando o refresh_token sem intervencao do usuario. O processo serializa chamadas concorrentes: se multiplos componentes chamam getToken simultaneamente enquanto um refresh esta em andamento, todos aguardam a mesma Promise para evitar multiplas chamadas ao token endpoint. Apos refresh bem-sucedido, o evento auth:token-refreshed e emitido e todos os callers recebem o novo access_token.

## Logout com Invalidacao de Sessao

O logout executa tres passos: primeiro remove todos os tokens do storage local (access_token, refresh_token, id_token, expires_at), depois redireciona para o end_session_endpoint do Keycloak com id_token_hint (para identificar a sessao) e post_logout_redirect_uri (para retornar a aplicacao apos logout). O Keycloak invalida a sessao server-side, garantindo que tokens existentes nao possam mais ser usados para refresh. O evento auth:logout e emitido para que a aplicacao limpe estado local.

## Extracao de Roles e Hierarquia

Claims do access_token JWT contem roles no path realm_access.roles como array de strings. O KeycloakClient extrai esses roles e os mapeia para o enum Role do tscore. A hierarquia de roles forma uma arvore com dois ramos sob MANAGER: o ramo de campo (FIELD_COORDINATOR supervisiona FIELD_CADASTRATOR) e o ramo de escritorio (ANALYST). MANAGER herda permissoes de ambos os ramos, ADMIN herda MANAGER, e SUPER_ADMIN herda ADMIN. O metodo hasRolePermission verifica autorizacao percorrendo a arvore: se o usuario tem role MANAGER e a funcionalidade requer FIELD_COORDINATOR, a verificacao retorna true pois MANAGER herda FIELD_COORDINATOR.

## Integracao com Frameworks

Hooks useAuth para React e composables useAuth para Vue encapsulam o KeycloakClient expondo estado reativo que atualiza automaticamente a UI quando tokens mudam. O AuthProvider (React) ou initAuth (Vue) inicializa o KeycloakClient na raiz da aplicacao e disponibiliza o contexto para toda a arvore de componentes. O ProtectedRoute (React) renderiza condicionalmente baseado em autenticacao e roles requeridas, redirecionando para login ou exibindo fallback quando sem permissao. Detalhes completos da API em [06-auth-api](../API/06-auth-api.md).
