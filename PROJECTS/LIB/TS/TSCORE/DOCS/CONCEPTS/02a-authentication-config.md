---
type: leaf
status: review
updated: 2026-02-08
---

# Autenticacao - Configuracao por Plataforma

Configuracoes especificas de tokens, storage, rotacao e client roles para cada plataforma do ecossistema CARF. Para o fluxo OAuth2 PKCE completo e gerenciamento de tokens ver [02-authentication](./02-authentication.md). Para a API programatica ver [06-auth-api](../API/06-auth-api.md) e [07-auth-native-api](../API/07-auth-native-api.md).

## Token Lifetimes

Configuracoes definidas no realm CARF do Keycloak. O access_token de 5 minutos forca refresh frequente, limitando a janela de comprometimento em caso de vazamento. Os lifetimes de refresh diferem por plataforma conforme necessidades operacionais de cada client.

| Token | Lifetime | Plataforma | Justificativa |
|:------|:---------|:-----------|:--------------|
| Access Token | 5 min | Todas | Janela curta de comprometimento |
| Refresh Token (web) | 30 min (SSO idle) | REURBWEB, ADMIN | Sessao de escritorio com inatividade limitada |
| Refresh Token (mobile) | 30 dias | REURBCAD | Agentes de campo sem acesso constante a internet |
| Refresh Token (desktop) | 30 dias | GEOGIS | Sessoes longas de georreferenciamento |
| SSO Session Max | 10 horas | Web | Limita duracao total de sessao web |

## Refresh Token Rotation

Atualmente rotation esta desabilitado no realm CARF. Cada refresh retorna o mesmo refresh_token ate sua expiracao. Recomendacao para producao: ativar rotation para mitigar token theft. Com rotation ativo, cada refresh invalida o token anterior e emite novo, permitindo deteccao de reuso como indicador de comprometimento. O KeycloakClient ja trata rotation corretamente, sempre armazenando o refresh_token retornado na response independente de ser novo ou o mesmo.

## Scope offline_access

O REURBCAD solicita scope offline_access explicitamente durante login para obter refresh tokens de longa duracao (30 dias). Este scope e habilitado apenas para os clients REURBCAD e GEOGIS no Keycloak, impedindo que aplicacoes web obtenham tokens de longa duracao acidentalmente. A duracao de 30 dias permite que agentes de campo facam login uma vez e mantenham sessao ativa durante toda a campanha de campo, realizando refreshes silenciosos sempre que necessario.

## Storage por Plataforma

A escolha de storage impacta diretamente a seguranca dos tokens. Cada plataforma usa o mecanismo mais seguro disponivel.

| Plataforma | Storage | Mecanismo | Seguranca |
|:-----------|:--------|:----------|:----------|
| REURBWEB (web) | WebStorageAdapter | localStorage para access_token (curta duracao) | Vulneravel a XSS; access_token de 5 min limita janela |
| ADMIN (web) | WebStorageAdapter | localStorage para access_token | Mesmo modelo do REURBWEB |
| REURBCAD (iOS) | MobileStorageAdapter | Keychain via expo-secure-store | Criptografado pelo SO, isolado por app |
| REURBCAD (Android) | MobileStorageAdapter | EncryptedSharedPreferences via expo-secure-store | Criptografia AES-256 pelo Android Keystore |
| GEOGIS (desktop) | QSettings adapter | QSettings do Qt em arquivo .ini protegido | Permissoes de arquivo do SO |

Para ambientes web de producao, a recomendacao e migrar refresh_token para HttpOnly cookies para eliminar exposicao a XSS. O access_token pode permanecer em memoria JavaScript pela curta duracao de 5 minutos, sendo re-obtido via refresh a cada carregamento de pagina.

## Client Roles

Alem dos realm roles hierarquicos (SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR), o Keycloak define client roles para controle granular de funcionalidades especificas por aplicacao. Client roles sao verificados pelo backend GEOAPI em endpoints especificos e pelo frontend via hasRole.

| Client Role | Descricao | Quem possui |
|:------------|:----------|:------------|
| manage-users | Criar, editar e desativar contas de usuario | ADMIN, SUPER_ADMIN |
| manage-tenants | Configurar tenants, isolamento e settings | SUPER_ADMIN |
| sync-data | Acessar Sync API para sincronizacao offline | FIELD_COORDINATOR, FIELD_CADASTRATOR |
| manage-team | Gerenciar membros e autorizacoes de equipe | FIELD_COORDINATOR, MANAGER |
| view-reports | Visualizar e exportar relatorios | ANALYST, MANAGER, ADMIN |
| manage-legitimation | Iniciar e gerenciar processos de legitimacao | ANALYST, MANAGER |
