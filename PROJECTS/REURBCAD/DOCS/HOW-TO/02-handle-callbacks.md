---
type: leaf
status: review
updated: 2026-02-08
---

# Handle OAuth Callbacks

## Visao Geral

Handle OAuth callbacks no REURBCAD requer configurar deep link listeners para receber authorization code apos usuario fazer login no Keycloak browser. `react-native-app-auth` e `expo-auth-session` fazem isso automaticamente, mas entender o mecanismo e util para debugging.

## Deep Link Flow

```
┌──────────┐     ┌─────────┐     ┌──────────┐     ┌────┐
│ REURBCAD │     │ Browser │     │ Keycloak │     │ OS │
└────┬─────┘     └────┬────┘     └────┬─────┘     └──┬─┘
     │ authorize()    │               │               │
     │───────────────>│ /auth?...     │               │
     │                │──────────────>│               │
     │                │  Login page   │               │
     │                │<──────────────│               │
     │                │  Submit login │               │
     │                │──────────────>│               │
     │                │  302 redirect │               │
     │                │  + code+state │               │
     │                │<──────────────│               │
     │                │               │  Deep link    │
     │                │───────────────│──────────────>│
     │  App launched / brought to foreground          │
     │<───────────────────────────────────────────────│
     │  Extract code + validate state                 │
     │  POST /token + code + code_verifier            │
     │───────────────────────────────>│               │
     │  { access_token, refresh_token }               │
     │<───────────────────────────────│               │
```

### Passos Detalhados

1. App faz `authorize(config)` que abre browser nativo
2. Browser navega para `http://localhost:8080/realms/carf/protocol/openid-connect/auth` com query params incluindo `redirect_uri=com.carf.reurbcad://oauth/callback`
3. Usuario completa login
4. Keycloak gera authorization code
5. Keycloak redirect browser para redirect_uri: `com.carf.reurbcad://oauth/callback?code=abc123&state=xyz789`
6. OS detecta deep link scheme `com.carf.reurbcad` e lanca app (se nao running) ou traz para foreground (se ja running)
7. App recebe deep link event via Linking API

## Configuracao Automatica (react-native-app-auth)

A library automaticamente:

1. Extrai `code` da URL query
2. Valida `state` param matches original para prevenir CSRF attacks
3. Faz POST ao token endpoint com `grant_type=authorization_code`, `client_id`, `code`, `code_verifier` (PKCE), `redirect_uri`
4. Recebe tokens response
5. Retorna promise que resolve com `{ accessToken, refreshToken, etc }`

## Implementacao Manual

Sem library, requer implementacao manual:

### Listener de Deep Link

```typescript
Linking.addEventListener('url', handleDeepLink);

const handleDeepLink = (event) => {
  const { url } = event;
  const params = extractParams(url);
  if (params.code && params.state === expectedState) {
    exchangeCodeForTokens(params.code)
      .then(tokens => storeTokens(tokens));
  }
};
```

### Extrair Parametros

```typescript
const extractParams = (urlString) => {
  const url = new URL(urlString);
  const searchParams = new URLSearchParams(url.search);
  return {
    code: searchParams.get('code'),
    state: searchParams.get('state')
  };
};
```

### Exchange Code por Tokens

```typescript
const exchangeCodeForTokens = async (code) => {
  const response = await fetch(
    'http://localhost:8080/realms/carf/protocol/openid-connect/token',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: 'reurbcad',
        code: code,
        code_verifier: originalVerifier,
        redirect_uri: 'com.carf.reurbcad://oauth/callback'
      })
    }
  );
  const tokens = await response.json();
  // { access_token, refresh_token, expires_in }
  await SecureStore.setItemAsync('refresh_token', tokens.refresh_token);
  return tokens;
};
```

### State Validation

State validation e critico para seguranca:

1. Gerar random string antes de authorize
2. Armazenar em memory ou AsyncStorage
3. Verificar que returned state matches expected
4. Previne CSRF onde attacker tricks user em clicar malicious deep link com different code

## Testing

### Android (via adb)

```bash
adb shell am start -a android.intent.action.VIEW \
  -d "com.carf.reurbcad://oauth/callback?code=test123"
```

Abre app com mock code - util para testar callback handling sem fazer login real.

### iOS (via xcrun)

```bash
xcrun simctl openurl booted \
  "com.carf.reurbcad://oauth/callback?code=test123"
```

Funciona no simulator.

## Edge Cases

### Callback Nunca Recebido

Se user fechou browser antes de completar login, promise de `authorize()` fica pending indefinitely. Mitigacao com timeout:

```typescript
const loginWithTimeout = () => Promise.race([
  authorize(config),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Login timeout')), 30000)
  )
]);

try {
  const result = await loginWithTimeout();
} catch (error) {
  // Mostra "Login cancelado" toast notification
}
```

### Multiple Callbacks

Se user taps back button no browser depois forward, pode gerar multiplos deep links com mesmo code. O code pode ser usado apenas uma vez no Keycloak, entao segundo callback falha com `"Code already used"`.

Mitigacao:

```typescript
let codeExchangeInProgress = false;

const handleDeepLink = async (event) => {
  if (codeExchangeInProgress) return; // previne duplicate exchanges
  codeExchangeInProgress = true;
  try {
    await exchangeCodeForTokens(extractCode(event.url));
  } finally {
    codeExchangeInProgress = false;
  }
};
```

### App Nao Instalado

Deep link so funciona se app instalado. Caso contrario, browser mostra erro "Page not found".

### Interstitial Android

Alguns browsers Android mostram interstitial "Open with REURBCAD app?" exigindo user confirmation. iOS ASWebAuthenticationSession nao mostra interstitial porque e sistema nativo.

## Seguranca

| Aspecto | Protecao |
|---|---|
| CSRF | State parameter validation |
| Code Interception | PKCE (code_verifier/code_challenge) |
| Token Exposure | SecureStore (Keychain/Keystore) |
| Replay Attack | Code single-use no Keycloak |
| Man-in-the-Middle | HTTPS obrigatorio em producao |

## Referencias

- [Setup Keycloak](./01-setup-keycloak.md)
- [Authentication](../CONCEPTS/01-authentication.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
