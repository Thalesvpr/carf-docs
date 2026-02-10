---
type: leaf
status: review
updated: 2026-02-08
---

# AuthService Layer

## Visao Geral

AuthService encapsula toda logica OAuth2 mobile em `src/services/AuthService.ts` como singleton class com private constructor garantindo single instance shared globalmente.

## Class Diagram

```
┌──────────────────────────────────────────────┐
│              AuthService (Singleton)          │
├──────────────────────────────────────────────┤
│ - instance: AuthService          [static]    │
│ - accessToken: string | null                 │
│ - refreshToken: string | null                │
│ - expiresAt: number | null                   │
├──────────────────────────────────────────────┤
│ + getInstance(): AuthService     [static]    │
│ + login(): Promise<User>                     │
│ + getAccessToken(): Promise<string>          │
│ + logout(): Promise<void>                    │
│ + restoreSession(): Promise<boolean>         │
│ + switchTenant(tenantId): Promise<void>      │
│ - _storeTokens(result): Promise<void>        │
│ - _loadUserInfo(): User                      │
└──────────────────────────────────────────────┘
```

## Configuracao

```typescript
const config = {
  issuer: KEYCLOAK_URL + '/realms/carf',
  clientId: 'reurbcad',
  redirectUrl: 'com.carf.reurbcad://oauth/callback',
  scopes: ['openid', 'profile', 'email', 'offline_access']
};
```

O scope `offline_access` e critico para obter long-lived refresh token.

## Propriedades

| Propriedade | Tipo | Armazenamento | Descricao |
|---|---|---|---|
| `accessToken` | `string \| null` | Memoria | Token de acesso JWT, curta duracao (5 min) |
| `refreshToken` | `string \| null` | SecureStore + Memoria | Token de refresh offline (30 dias) |
| `expiresAt` | `number \| null` | Memoria | Timestamp de expiracao do access token |

## Metodos

### login()

| Aspecto | Detalhe |
|---|---|
| **Retorno** | `Promise<User>` |
| **Descricao** | Abre browser nativo, usuario faz login no Keycloak, retorna User |

Implementacao:

```typescript
async login(): Promise<User> {
  const result = await authorize(config);
  // Abre ASWebAuthenticationSession (iOS) ou Chrome Custom Tabs (Android)
  // result: { accessToken, idToken, refreshToken, accessTokenExpirationDate }

  await this._storeTokens(result);
  return this._loadUserInfo();
}
```

`_storeTokens()` executa:
- `await SecureStore.setItemAsync('refresh_token', result.refreshToken)` - encrypted via Keychain/Keystore
- `this.accessToken = result.accessToken`
- `this.expiresAt = new Date(result.accessTokenExpirationDate).getTime()`

`_loadUserInfo()` decodifica JWT parseando base64 payload extraindo claims: `sub`, `email`, `name`, `tenant_id`, `allowed_tenants`, `roles`. Retorna User object.

### getAccessToken()

| Aspecto | Detalhe |
|---|---|
| **Retorno** | `Promise<string>` |
| **Descricao** | Retorna access token valido, fazendo refresh se necessario |

Implementacao:

```typescript
async getAccessToken(): Promise<string> {
  // Token ainda valido por mais de 1 minuto?
  if (Date.now() < this.expiresAt - 60000) {
    return this.accessToken;
  }

  if (!this.refreshToken) {
    throw new Error('No refresh token');
  }

  // Refresh necessario
  const result = await refresh(config, {
    refreshToken: this.refreshToken
  });
  // POST ao token endpoint com grant_type=refresh_token

  await this._storeTokens(result);
  return this.accessToken;
}
```

Se refresh falha, chama `this.logout()` limpando tokens e lancando error forcando re-login.

### logout()

| Aspecto | Detalhe |
|---|---|
| **Retorno** | `Promise<void>` |
| **Descricao** | Revoga token no Keycloak e limpa armazenamento local |

Implementacao:

```typescript
async logout(): Promise<void> {
  // Revogar server-side
  await revoke(config, {
    tokenToRevoke: this.refreshToken,
    tokenTypeHint: 'refresh_token'
  });
  // POST ao revoke endpoint invalidando token

  // Limpar local
  await SecureStore.deleteItemAsync('refresh_token');
  this.accessToken = null;
  this.refreshToken = null;
  this.expiresAt = null;

  // Notificar UI
  // Lanca AuthLogoutEvent para listeners notificarem UI update
}
```

### restoreSession()

| Aspecto | Detalhe |
|---|---|
| **Retorno** | `Promise<boolean>` |
| **Descricao** | Restaura sessao no app startup, retorna true se autenticado |

Implementacao:

```typescript
async restoreSession(): Promise<boolean> {
  const refreshToken = await SecureStore.getItemAsync('refresh_token');
  if (!refreshToken) return false; // no session

  this.refreshToken = refreshToken;

  try {
    await this.getAccessToken(); // faz refresh automatico validando token
    return true; // authenticated
  } catch {
    return false; // forca login
  }
}
```

### switchTenant()

| Aspecto | Detalhe |
|---|---|
| **Parametros** | `tenantId: string` |
| **Retorno** | `Promise<void>` |
| **Descricao** | Troca tenant ativo, limpa dados locais, re-sincroniza |

Implementacao:

```typescript
async switchTenant(tenantId: string): Promise<void> {
  // Validar se tenant permitido
  if (!this.user.allowed_tenants.includes(tenantId)) {
    throw new Error('Tenant not allowed');
  }

  // Atualizar no backend
  const token = await this.getAccessToken();
  await fetch('/api/auth/switch-tenant', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ tenantId })
  });
  // Backend atualiza current_tenant attribute no Keycloak user

  // Forcar refresh para obter novo token com tenant_id atualizado
  this.expiresAt = 0; // bypass cache
  await this.getAccessToken();

  // Retorna success
}
```

## Usage Patterns

### Em Screens

```typescript
const authService = AuthService.getInstance();

// Login button tap
await authService.login()
  .then(user => navigation.replace('Home'))
  .catch(err => Alert.alert('Erro', err.message));
```

### Axios Interceptors

#### Request Interceptor

Adiciona Authorization header automaticamente antes de cada request, garantindo token valido (refreshando se necessario):

```typescript
axios.interceptors.request.use(async (config) => {
  config.headers.Authorization =
    'Bearer ' + await AuthService.getInstance().getAccessToken();
  return config;
});
```

#### Response Interceptor

Se status 401, tenta refresh uma vez; se falha, forca logout redirecionando para login:

```typescript
axios.interceptors.response.use(
  response => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const token = await AuthService.getInstance().getAccessToken();
        error.config.headers.Authorization = `Bearer ${token}`;
        return axios(error.config); // retry
      } catch {
        await AuthService.getInstance().logout();
        // Redirect para login
      }
    }
    return Promise.reject(error);
  }
);
```

## Referencias

- [Authentication](../CONCEPTS/01-authentication.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
- [Secure Storage](../CONCEPTS/03-secure-storage.md)
- [Setup Keycloak](../HOW-TO/01-setup-keycloak.md)
