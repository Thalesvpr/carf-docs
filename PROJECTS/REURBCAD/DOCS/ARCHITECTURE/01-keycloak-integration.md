---
type: leaf
status: review
updated: 2026-02-08
---

# Integracao Keycloak Mobile

## Visao Geral

REURBCAD integra Keycloak mobile usando `react-native-app-auth` (bare RN) ou `expo-auth-session` (Expo) implementando OAuth2 Authorization Code + PKCE flow.

## Configuracao de Deep Link

### app.json (Expo)

```json
{
  "expo": {
    "scheme": "carf"
  }
}
```

### AndroidManifest.xml (Bare RN)

```xml
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.BROWSABLE" />
  <category android:name="android.intent.category.DEFAULT" />
  <data
    android:scheme="carf"
    android:host="oauth"
    android:pathPrefix="/callback" />
</intent-filter>
```

### Info.plist (iOS)

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>carf</string>
    </array>
  </dict>
</array>
```

## Configuracao OAuth

AuthService class encapsula logica OAuth criando config object:

```typescript
const config = {
  issuer: KEYCLOAK_URL + '/realms/carf',
  clientId: 'reurbcad',
  redirectUrl: 'carf://oauth/callback',
  scopes: ['openid', 'profile', 'email', 'offline_access']
};
```

O scope `offline_access` e critico para obter refresh token de longa duracao permitindo sync em background.

| Parametro | Valor | Descricao |
|---|---|---|
| `issuer` | `KEYCLOAK_URL/realms/carf` | URL do realm Keycloak |
| `clientId` | `reurbcad` | Client ID configurado no Keycloak |
| `redirectUrl` | `carf://oauth/callback` | Deep link de retorno |
| `scopes` | `openid, profile, email, offline_access` | Escopos solicitados |

## Login Flow

O metodo `login()` chama `authorize(config)` que abre browser nativo via ASWebAuthenticationSession (iOS) ou Chrome Custom Tabs (Android) navegando para Keycloak login screen. O fluxo segue:

1. Usuario faz login no browser nativo
2. Keycloak gera authorization code
3. Redirect de volta para app via deep link com code
4. Library automaticamente exchange code por tokens enviando `code_verifier` para PKCE validation
5. Retorna `{ accessToken, idToken, refreshToken, accessTokenExpirationDate }`
6. Armazena tokens com `SecureStore.setItemAsync('refresh_token', refreshToken)` - nunca AsyncStorage porque plain text e inseguro
7. Mantem `accessToken` e `expiresAt` em memoria (class properties)

## Token Management

### getAccessToken()

Checa `if (Date.now() < expiresAt - 60000)` e retorna `accessToken` cached. Caso contrario faz refresh chamando `refresh(config, { refreshToken })` obtendo novo `accessToken`, atualizando `expiresAt` e opcionalmente novo `refreshToken`.

Se refresh falha (offline token expirou apos 30 dias), forca logout redirecionando para login.

### API Interceptor

API calls usam interceptor que adiciona Authorization header obtendo token com `await AuthService.getAccessToken()` antes de cada request. Se request retorna 401, tenta refresh uma vez; se falha novamente, forca logout.

## Logout

O metodo `logout()`:

1. Chama `revoke(config, { tokenToRevoke: refreshToken })` invalidando token no Keycloak
2. Limpa tokens local com `SecureStore.deleteItemAsync()`

### Restore Session

`restoreSession()` chamado no app startup:

1. Tenta obter `refresh_token` do SecureStore
2. Se existe, tenta refresh para obter `accessToken` valido
3. Se sucesso, usuario ja logado
4. Se falha, forca login

## Tenant Switching

Tenant switching implementado fazendo `POST /api/auth/switch-tenant` no backend com novo `tenantId`:

1. Backend valida `allowed_tenants` claim e atualiza `current_tenant` no Keycloak
2. Frontend forca refresh com `getAccessToken()` passando flag para bypass cache obtendo novo token com `tenant_id` claim atualizado
3. Limpa WatermelonDB local com `database.write(async () => { await database.unsafeResetDatabase() })` para evitar mixing de dados de diferentes tenants
4. Re-sincroniza dados do novo tenant via `syncData()`

## Offline Tokens

Offline tokens sao criticos porque field collectors trabalham em areas sem internet. O refresh token deve durar 30 dias, configurado no Keycloak realm settings:

- **Offline Session Idle**: 30 days

Isso permite sync quando voltam para area com conexao.

## Referencias

- [Keycloak Integration Central](../../../CENTRAL/ARCHITECTURE/INTEGRATION/01-authentication.md)
- [AuthService Layer](../LAYERS/01-auth-service.md)
- [Secure Storage](../CONCEPTS/03-secure-storage.md)
