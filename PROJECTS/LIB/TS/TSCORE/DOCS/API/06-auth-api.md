---
type: leaf
status: review
updated: 2026-02-08
---

# API de Autenticacao

Documentacao completa do cliente Keycloak e hooks de autenticacao exportados pelos modulos @carf/tscore/auth, @carf/tscore/auth/react e @carf/tscore/auth/vue. O sistema implementa OAuth2 Authorization Code com PKCE conforme descrito em [02-authentication](../CONCEPTS/02-authentication.md), com storage cross-platform via adapters documentados em [07-auth-native-api](./07-auth-native-api.md).

## KeycloakConfig

Interface de configuracao obrigatoria para instanciacao do KeycloakClient.

| Propriedade | Tipo TS | Obrigatorio | Descricao |
|:------------|:--------|:------------|:----------|
| keycloakUrl | string | sim | URL do servidor Keycloak (ex: https://auth.carf.gov.br) |
| realm | string | sim | Nome do realm, padrao "carf" |
| clientId | string | sim | Client ID registrado no Keycloak (geoweb-client, reurbcad-client, admin-client) |
| redirectUri | string | sim | URI de callback apos autenticacao |
| scope | string | nao | Scopes adicionais separados por espaco, ex: "openid profile offline_access" |
| storage | StorageAdapter | nao | Adapter de storage customizado, auto-detectado se omitido |
| navigation | NavigationAdapter | nao | Adapter de navegacao customizado, auto-detectado se omitido |

## KeycloakClient

Classe principal para autenticacao OAuth2 com Keycloak. Gerencia ciclo de vida completo de tokens com refresh automatico, extracao de roles do JWT e verificacao de permissoes hierarquicas.

### Metodos

| Metodo | Parametros | Retorno | Descricao |
|:-------|:-----------|:--------|:----------|
| init | config: KeycloakConfig | Promise de void | Inicializa o cliente carregando tokens do storage e verificando validade. Executa refresh se access_token expirado e refresh_token valido. Emite evento auth:initialized ao concluir. |
| login | options?: LoginOptions | Promise de void | Gera code_verifier (128 chars), calcula code_challenge SHA-256 base64url, armazena verifier e state no storage, redireciona para authorize endpoint do Keycloak com response_type code, client_id, redirect_uri, code_challenge, code_challenge_method S256, scope e state. |
| handleCallback | url?: string | Promise de AuthTokens | Extrai code e state da URL de callback, valida state contra armazenado, envia POST para token endpoint com grant_type authorization_code, code, redirect_uri, client_id e code_verifier. Armazena tokens retornados e emite auth:login. |
| logout | | Promise de void | Limpa tokens do storage, redireciona para end_session_endpoint do Keycloak com id_token_hint e post_logout_redirect_uri para invalidar sessao server-side. Emite auth:logout. |
| getToken | | Promise de string | Retorna access_token valido do cache. Se expirado ou proximo de expirar (margem 5 min), executa refresh transparente via refresh_token. Se refresh falha, limpa storage e lanca AuthExpiredError. |
| refreshToken | | Promise de AuthTokens | Forca refresh enviando grant_type refresh_token ao token endpoint. Armazena novos tokens. Com rotation ativo, o refresh_token anterior e invalidado. |
| hasRole | role: Role | boolean | Verifica se usuario possui role especifica no claim realm_access.roles do JWT. |
| hasRolePermission | requiredRole: Role | boolean | Verifica permissao considerando hierarquia: SUPER_ADMIN herda ADMIN que herda MANAGER que herda ANALYST e FIELD_COORDINATOR que herda FIELD_CADASTRATOR. |
| getUserInfo | | User | Extrai dados do usuario do JWT: id (sub), username (preferred_username), email, name, roles (realm_access.roles), tenantId (custom claim tenant_id). |
| isAuthenticated | | boolean | Retorna true se access_token ou refresh_token valido existe no storage. |
| onAuthStateChange | callback: (event: AuthEvent) => void | Unsubscribe | Registra listener para eventos de autenticacao: auth:initialized, auth:login, auth:logout, auth:token-refreshed, auth:session-expired. Retorna funcao de unsubscribe. |

### AuthTokens

Interface contendo tokens retornados pelo Keycloak.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| accessToken | string | JWT para autorizacao nas APIs |
| refreshToken | string | Token para renovacao do access_token |
| idToken | string | JWT com dados do usuario |
| expiresAt | number | Timestamp Unix (segundos) de expiracao do access_token |

### User

Interface representando usuario autenticado extraido do JWT.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| id | string | UUID do usuario (claim sub) |
| username | string | Nome de usuario (preferred_username) |
| email | string | Email do usuario |
| name | string | Nome completo |
| roles | array de Role | Roles do realm |
| tenantId | string | UUID do tenant (custom claim) |

## React Hooks

O hook useAuth retorna objeto com user (User ou null), isLoading (boolean durante init), isAuthenticated (boolean), login (funcao async), logout (funcao async), hasRole (funcao com role), hasPermission (funcao com role considerando hierarquia) e getToken (funcao async retornando string). O componente AuthProvider recebe instancia de KeycloakClient como prop client e fornece contexto para toda a arvore de componentes React. O componente ProtectedRoute aceita props roles (array de Role requeridas) e fallback (componente exibido quando sem permissao), renderizando children apenas se autenticado e com pelo menos uma das roles requeridas. O hook useUser retorna User do usuario atual, lancando erro se chamado fora de AuthProvider. O hook usePermissions retorna objeto com propriedades isAdmin (boolean), isManager (boolean), isAnalyst (boolean), isCoordinator (boolean) e isCadastrator (boolean) computadas a partir dos roles do usuario.

## Vue Composables

O composable useAuth retorna refs reativas user, isLoading e isAuthenticated, alem de funcoes login, logout, hasRole, hasPermission e getToken com mesma semantica dos hooks React. A funcao initAuth recebe instancia de KeycloakClient e app Vue, registrando o cliente como provide global. O composable usePermissions fornece computed properties isAdmin, isManager, isAnalyst, isCoordinator e isCadastrator.
