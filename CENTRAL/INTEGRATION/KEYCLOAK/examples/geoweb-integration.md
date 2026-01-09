# GEOWEB + Keycloak (React)

## Install
```bash
npm install keycloak-js
```

## Config
```typescript
// src/config/keycloak.ts
import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL,
  realm: 'carf',
  clientId: 'geoweb',
});

export default keycloak;
```

## Auth Provider
```typescript
// src/providers/AuthProvider.tsx
const AuthProvider = ({ children }) => {
  useEffect(() => {
    keycloak.init({ onLoad: 'check-sso', pkceMethod: 'S256' })
      .then(authenticated => setAuth(authenticated));

    keycloak.onTokenExpired = () => keycloak.updateToken(300);
  }, []);

  return <AuthContext.Provider value={{ ...auth }}>{children}</AuthContext.Provider>;
};
```

## Protected Route
```typescript
const PrivateRoute = ({ children, role }) => {
  const { isAuthenticated, hasRole } = useAuth();

  if (!isAuthenticated) return <Navigate to="/login" />;
  if (role && !hasRole(role)) return <Navigate to="/unauthorized" />;

  return children;
};
```

## API Calls
```typescript
// src/lib/api.ts
import axios from 'axios';

const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use(async config => {
  if (keycloak.isTokenExpired(30)) await keycloak.updateToken(30);
  config.headers.Authorization = `Bearer ${keycloak.token}`;
  return config;
});

export default api;
```

## Tenant Switcher
```typescript
const TenantSwitcher = () => {
  const { tenantId, allowedTenants, switchTenant } = useAuth();

  return (
    <select value={tenantId} onChange={e => switchTenant(e.target.value)}>
      {allowedTenants.map(t => <option key={t} value={t}>{t}</option>)}
    </select>
  );
};
```

## Get Claims
```typescript
const token = keycloak.tokenParsed;
const tenantId = token?.tenant_id;
const roles = keycloak.realmAccess?.roles || [];
```

Done. ✅
