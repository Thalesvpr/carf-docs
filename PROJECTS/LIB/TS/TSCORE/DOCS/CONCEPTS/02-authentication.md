---
type: leaf
status: review
updated: 2026-01-24
---

# Autenticacao

Sistema de autenticacao integrado com Keycloak usando OAuth2 Authorization Code com PKCE. O KeycloakClient gerencia ciclo de vida completo de tokens com refresh automatico e extracao de roles.

## Fluxo OAuth2 PKCE

O fluxo inicia quando aplicacao chama login. Cliente gera code_verifier aleatorio de 128 caracteres e deriva code_challenge usando SHA-256 base64url. Redireciona para Keycloak com client_id, redirect_uri, code_challenge, code_challenge_method S256 e state aleatorio para prevenir CSRF. Usuario autentica no Keycloak que redireciona de volta com authorization code e state.

A aplicacao valida state, extrai code e chama handleCallback. Cliente envia code e code_verifier para token endpoint. Keycloak verifica se hash do code_verifier corresponde ao code_challenge original. Se valido, retorna access_token, refresh_token e id_token. Cliente armazena tokens e extrai claims do JWT.

## Gerenciamento de Tokens

O metodo getToken verifica expiracao do access_token. Se expirado ou proximo de expirar, executa refresh usando refresh_token. Renovacao ocorre transparentemente sem intervencao do usuario. Tokens sao armazenados em storage configuravel via StorageAdapter para suporte cross-platform.

## Extracao de Roles

Claims do access_token contem roles no path realm_access.roles ou resource_access[clientId].roles. O cliente extrai roles e mapeia para enum Role do tscore. Verificacao hierarquica usa tabela de niveis onde SUPER_ADMIN tem nivel maximo e FIELD_CADASTRATOR nivel minimo. FIELD_COORDINATOR supervisiona equipe de campo com acesso completo ao menu mobile, enquanto FIELD_CADASTRATOR tem acesso restrito apenas ao mapa e formularios. Funcao hasRolePermission compara niveis para autorizacao.

## Integracao com Frameworks

Hooks useAuth para React e composables useAuth para Vue encapsulam KeycloakClient expondo estado reativo. AuthProvider e initAuth inicializam contexto na raiz da aplicacao. ProtectedRoute renderiza condicionalmente baseado em autenticacao e roles requeridas.
