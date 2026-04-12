---
type: leaf
status: review
updated: 2026-02-08
---

# Setup Keycloak no REURBCAD

## Pre-Requisitos

- Node.js 18+
- React Native CLI ou Expo CLI
- Docker (para Keycloak local)
- Keycloak realm `carf` configurado

## Passo 1: Instalar Dependencias

**Bare React Native:**

```bash
npm install react-native-app-auth
```

**Expo Managed:**

Usar `expo-auth-session` (incluso no Expo SDK).

## Passo 2: Configurar .env

Criar arquivo `.env` na raiz do projeto:

```env
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=carf
KEYCLOAK_CLIENT_ID=reurbcad
API_URL=http://localhost:5000
```

## Passo 3: Configurar Deep Link Scheme

### app.json (Expo)

Adicionar `"scheme"` dentro do objeto `expo`:

```json
{
  "expo": {
    "scheme": "com.carf.reurbcad"
  }
}
```

### AndroidManifest.xml (Bare RN)

Adicionar `<intent-filter>` dentro de `<activity android:name=".MainActivity">`:

```xml
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data
    android:scheme="com.carf.reurbcad"
    android:host="oauth"
    android:pathPrefix="/callback" />
</intent-filter>
```

### Info.plist (iOS Bare)

Adicionar URL scheme:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>com.carf.reurbcad</string>
    </array>
  </dict>
</array>
```

## Passo 4: Criar AuthService

Criar `src/services/AuthService.ts` com config object:

```typescript
import { authorize, refresh, revoke } from 'react-native-app-auth';
import * as SecureStore from 'expo-secure-store';

const config = {
  issuer: process.env.KEYCLOAK_URL + '/realms/' + process.env.KEYCLOAK_REALM,
  clientId: process.env.KEYCLOAK_CLIENT_ID,
  redirectUrl: 'com.carf.reurbcad://oauth/callback',
  scopes: ['openid', 'profile', 'email', 'offline_access']
};
```

### Metodo login()

```typescript
async login() {
  const result = await authorize(config);
  // Abre browser, usuario faz login, retorna tokens
  // result: { accessToken, idToken, refreshToken, accessTokenExpirationDate }

  await SecureStore.setItemAsync('refresh_token', result.refreshToken);
  this.accessToken = result.accessToken;
  this.expiresAt = new Date(result.accessTokenExpirationDate).getTime();
}
```

### Metodo getAccessToken()

```typescript
async getAccessToken() {
  if (Date.now() < this.expiresAt - 60000) {
    return this.accessToken; // cached, valido por mais de 1 min
  }
  const result = await refresh(config, { refreshToken: this.refreshToken });
  // Atualiza tokens
  this.accessToken = result.accessToken;
  this.expiresAt = new Date(result.accessTokenExpirationDate).getTime();
  return this.accessToken;
}
```

### Metodo logout()

```typescript
async logout() {
  await revoke(config, { tokenToRevoke: this.refreshToken });
  await SecureStore.deleteItemAsync('refresh_token');
}
```

### Metodo restoreSession()

Chamado no app startup:

```typescript
async restoreSession(): Promise<boolean> {
  const refreshToken = await SecureStore.getItemAsync('refresh_token');
  if (!refreshToken) return false;

  try {
    this.refreshToken = refreshToken;
    await this.getAccessToken(); // faz refresh para validar
    return true;
  } catch {
    return false;
  }
}
```

## Passo 5: Criar AuthContext

Criar `src/contexts/AuthContext.tsx`:

```typescript
const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    restoreSession()
      .then(authenticated => setIsAuthenticated(authenticated))
      .finally(() => setIsLoading(false));
  }, []);

  // Provider value exporta:
  // { user, isAuthenticated, isLoading, login, logout, getAccessToken }
  return (
    <AuthContext.Provider value={...}>
      {children}
    </AuthContext.Provider>
  );
};
```

## Passo 6: Configurar Navigation

Em `App.tsx`, importar AuthProvider e wrap:

```tsx
<AuthProvider>
  <Navigation />
</AuthProvider>
```

Em `src/navigation/index.tsx`, criar stack navigator:

```typescript
const Stack = createNativeStackNavigator();

// Conditional rendering
{isAuthenticated ? <AppStack /> : <AuthStack />}
```

Onde `AppStack` tem screens protegidas e `AuthStack` tem LoginScreen.

## Passo 7: Criar LoginScreen

```tsx
const LoginScreen = () => {
  const { login } = useAuth();
  return <Button onPress={login} title="Entrar com Keycloak" />;
};
```

## Passo 8: Configurar Keycloak Local

1. Iniciar Keycloak: `docker-compose up -d`
2. Verificar realm `carf` e client `reurbcad` configurado:

| Configuracao | Valor |
|---|---|
| Valid Redirect URIs | `com.carf.reurbcad://oauth/callback` |
| Web Origins | `+` |
| Public Client | ON |
| Standard Flow Enabled | ON |
| PKCE Code Challenge Method | S256 |

3. Criar user teste via Admin Console:
   - Username, email, password (temporary OFF)
   - Attributes: `tenants=["prefeitura-teste"]`, `current_tenant=["prefeitura-teste"]`
   - Role mappings: `field-cadastrator` (only map and forms, no menu) ou `field-coordinator` (supervises field team, full mobile menu)

## Passo 9: Testar

1. Iniciar app com `npx react-native run-android` ou `npx expo start`
2. Tap botao Login
3. Observar browser abrindo para Keycloak login
4. Fazer login com user teste
5. Observar redirect de volta para app via deep link
6. Verificar logs `"Token validated for user..."` indicando sucesso

## Verificacao

- [ ] SecureStore contem refresh_token: `SecureStore.getItemAsync('refresh_token').then(console.log)`
- [ ] Token refresh funciona: fechar app, esperar 6+ minutos para access_token expirar, reabrir app, verificar que `restoreSession()` sucede fazendo refresh automatico
- [ ] Deep link callback funciona corretamente
- [ ] Logout limpa todos os tokens

## Referencias

- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
- [Handle Callbacks](./02-handle-callbacks.md)
- [AuthService Layer](../LAYERS/01-auth-service.md)
