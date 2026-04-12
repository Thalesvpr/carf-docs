---
type: leaf
status: review
updated: 2026-02-08
---

# Autenticacao OAuth2 PKCE no REURBCAD Mobile

## Visao Geral

Authentication no REURBCAD mobile usa OAuth2 Authorization Code + PKCE flow adaptado para mobile. O app abre browser nativo (nao webview) via `react-native-app-auth` ou `expo-auth-session`, mantendo session cookies isolados do app e aumentando seguranca.

## PKCE Flow

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│ REURBCAD │    │ Browser Nat. │    │ Keycloak │
└────┬─────┘    └──────┬───────┘    └────┬─────┘
     │  authorize()    │                 │
     │────────────────>│  /auth?...      │
     │                 │────────────────>│
     │                 │   Login Screen  │
     │                 │<────────────────│
     │                 │  User submits   │
     │                 │────────────────>│
     │                 │  redirect_uri   │
     │                 │  + code + state │
     │  Deep link      │<────────────────│
     │<────────────────│                 │
     │  POST /token                      │
     │  + code + code_verifier           │
     │──────────────────────────────────>│
     │  { access_token, refresh_token }  │
     │<──────────────────────────────────│
```

### Passos Detalhados

1. App abre browser nativo navegando para Keycloak login screen
2. Usuario faz login com credenciais
3. Keycloak gera authorization code
4. Redirect via deep link com scheme `com.carf.reurbcad://oauth/callback`
5. App recebe deep link event via `Linking.addEventListener('url', handleDeepLink)`
6. Extrai code da URL query params
7. Library automaticamente exchange code por tokens fazendo POST ao `/protocol/openid-connect/token` com:
   - `grant_type=authorization_code`
   - `client_id=reurbcad`
   - `code`
   - `code_verifier` (PKCE)
   - `redirect_uri`
8. Recebe JSON response: `{ access_token, id_token, refresh_token, expires_in, refresh_expires_in }`

## Token Storage

Armazena `refresh_token` em SecureStore com encryption via Keychain (iOS) ou Keystore (Android):

```typescript
await SecureStore.setItemAsync('refresh_token', refreshToken);
```

Mantem `accessToken` e `expiresAt` em memoria como class properties do AuthService.

> **Nunca** usar AsyncStorage para tokens - plain text acessivel via device backup, root/jailbreak, ou malware.

## Claims Extraction

`parseUser()` method decodifica accessToken JWT extraindo claims:

```typescript
const payload = atob(token.split('.')[1]);
const claims = JSON.parse(payload);
// { sub, email, name, tenant_id, allowed_tenants, realm_access.roles }
```

## Refresh Strategy

Token refresh implementado em `getAccessToken()`:

```typescript
if (Date.now() < this.expiresAt - 60000) {
  return this.accessToken; // cached, ainda valido
}
// Refresh necessario
const result = await POST('/protocol/openid-connect/token', {
  grant_type: 'refresh_token',
  client_id: 'reurbcad',
  refresh_token: this.refreshToken
});
this.accessToken = result.access_token;
this.expiresAt = Date.now() + (result.expires_in * 1000);
```

Se refresh falha (offline token expirado apos 30 dias), chama `logout()` limpando tokens e redirecionando para login.

## Offline Access

O scope `offline_access` e critico para obter offline refresh token com validade estendida:

| Token | Duracao | Configuracao Keycloak |
|---|---|---|
| Access Token | 5 minutos | Realm > Tokens > Access Token Lifespan |
| Refresh Token (offline) | 30 dias idle / 60 dias max | Realm > Sessions > Offline Session Idle / Max |

Permite field collectors trabalhar semanas sem re-login mesmo offline, porque quando voltam online o refresh ainda e valido.

## Session Restoration

`restoreSession()` no app startup:

1. Tenta obter `refresh_token` do SecureStore
2. Se existe, tenta refresh para validar
3. Se sucesso, popula user state e considera `authenticated=true`
4. Se falha ou token nao existe, mostra login screen

## Logout

Implementado com revoke server-side + limpeza local:

```typescript
// Revoke no Keycloak
await revoke(config, { tokenToRevoke: refreshToken });
// POST /protocol/openid-connect/revoke

// Limpar local
await SecureStore.deleteItemAsync('refresh_token');
this.accessToken = null;
this.refreshToken = null;
```

## API Interceptor (Axios)

Interceptor que garante token valido antes de cada request:

```typescript
// Request interceptor
axios.interceptors.request.use(async (config) => {
  const accessToken = await AuthService.getAccessToken();
  config.headers.Authorization = `Bearer ${accessToken}`;
  return config;
});
```

Se response 401, tenta refresh uma vez; se falha novamente, forca logout.

## Offline Queue

Quando `NetInfo.isConnected=false`, API calls sao queued localmente em AsyncStorage com `pending_requests` array:

```typescript
{
  url: string,
  method: string,
  body: object,
  headers: object,
  timestamp: number
}
```

Quando conexao restabelecida, processa queue sequencialmente com retry e exponential backoff para failed requests.

## Referencias

- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
- [Offline Authentication](./02-offline-authentication.md)
- [Secure Storage](./03-secure-storage.md)
- [AuthService Layer](../LAYERS/01-auth-service.md)
