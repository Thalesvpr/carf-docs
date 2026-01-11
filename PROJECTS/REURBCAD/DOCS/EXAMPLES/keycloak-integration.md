# REURBCAD + Keycloak (React Native)

## Install
```bash
npm install react-native-app-auth react-native-keychain
npx pod-install # iOS only
```

## Config
```typescript
// src/config/keycloak.ts
export const keycloakConfig = {
  issuer: 'http://localhost:8080/realms/carf',
  clientId: 'reurbcad',
  redirectUrl: 'carf://callback',
  scopes: ['openid', 'profile', 'email', 'offline_access'],
};
```

## Auth Hook
```typescript
// src/hooks/useKeycloakAuth.ts
import { authorize, refresh, revoke } from 'react-native-app-auth';
import * as Keychain from 'react-native-keychain';

export const useKeycloakAuth = () => {
  const [authState, setAuthState] = useState(null);

  const login = async () => {
    const result = await authorize(keycloakConfig);
    await Keychain.setGenericPassword('token', JSON.stringify(result));
    setAuthState(result);
  };

  const logout = async () => {
    if (authState) await revoke(keycloakConfig, { tokenToRevoke: authState.refreshToken });
    await Keychain.resetGenericPassword();
    setAuthState(null);
  };

  const refreshToken = async () => {
    const result = await refresh(keycloakConfig, { refreshToken: authState.refreshToken });
    await Keychain.setGenericPassword('token', JSON.stringify(result));
    setAuthState(result);
  };

  return { authState, login, logout, refreshToken };
};
```

## API Calls
```typescript
// src/lib/api.ts
import axios from 'axios';

const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use(async config => {
  const creds = await Keychain.getGenericPassword();
  if (creds) {
    const auth = JSON.parse(creds.password);
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});
```

## Deep Link (iOS)
```xml
<!-- ios/reurbcad/Info.plist -->
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

## Deep Link (Android)
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="carf" />
</intent-filter>
```

Done. ✅
