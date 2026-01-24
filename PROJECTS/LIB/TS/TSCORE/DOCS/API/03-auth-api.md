---
type: leaf
status: review
updated: 2026-01-24
---

# API de Autenticacao

Documentacao do cliente Keycloak e hooks de autenticacao exportados pelos modulos @carf/tscore/auth, @carf/tscore/auth/react e @carf/tscore/auth/vue.

## KeycloakClient

Classe principal para autenticacao OAuth2 com Keycloak. O construtor recebe KeycloakConfig com url do servidor, realm e clientId. O metodo init carrega tokens de storage e verifica validade. O metodo login redireciona para Keycloak usando Authorization Code com PKCE gerando code_verifier e code_challenge. O metodo handleCallback processa retorno OAuth trocando code por tokens. O metodo logout limpa sessao local e redireciona para logout do Keycloak.

O metodo getToken retorna access token valido, executando refresh automatico quando expiracao se aproxima. O metodo getUser retorna objeto User com id, username, email, name e roles extraidos do JWT. O metodo hasRole verifica se usuario possui role especifica. O metodo hasRolePermission verifica permissao considerando hierarquia de roles. O metodo isAuthenticated retorna boolean indicando sessao ativa.

## React Hooks

O hook useAuth retorna objeto com user, isLoading, isAuthenticated, login, logout, hasRole, hasPermission e getToken. O componente AuthProvider recebe KeycloakClient e fornece contexto para arvore de componentes. O componente ProtectedRoute renderiza children apenas se autenticado e com roles requeridas, exibindo fallback caso contrario. O hook useUser retorna dados do usuario atual. O hook usePermissions oferece verificacoes de role com propriedades isAdmin e isManager.

## Vue Composables

O composable useAuth retorna refs reativas user, isLoading e isAuthenticated alem de funcoes login, logout, hasRole, hasPermission e getToken. A funcao initAuth registra cliente no app Vue. O composable usePermissions fornece verificacoes de role com computed properties.

## Tipos de Suporte

KeycloakConfig define configuracao de conexao com url, realm e clientId. User representa usuario autenticado com roles e tenantId. AuthTokens armazena accessToken, refreshToken, idToken e expiresAt como timestamp.
