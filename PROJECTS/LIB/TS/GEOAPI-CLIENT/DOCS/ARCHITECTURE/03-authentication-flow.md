# Authentication Flow - @carf/geoapi-client

## Fluxo de Autenticação

Authentication flow no @carf/geoapi-client usa [OAuth2 Authorization Code](https://oauth.net/2/grant-types/authorization-code/) + PKCE via `@carf/tscore` KeycloakClient (ver TSCORE/DOCS/CONCEPTS/02-authentication) conforme integração documentada em , cliente HTTP recebe instância de `AuthClient` no construtor armazenando reference para buscar access token antes de cada request, interceptor axios adiciona header `Authorization: Bearer ${token}` automaticamente em todas as requisições chamando `authClient.getAccessToken()` que retorna token cached se válido ou faz refresh se expirado usando refresh_token, se refresh falha (401 Unauthorized ou refresh_token expirado) interceptor emite evento `auth:session-expired` para aplicação consumidora redirecionar para login, requests com 401 são automaticamente retried UMA VEZ após refresh token, requests com 403 Forbidden não são retried (usuário não tem permissão), e logout limpa tokens chamando `authClient.logout()` que invalida sessão no Keycloak e remove tokens do storage.

## Diagrama de Fluxo

```
┌─────────────┐
│ GEOWEB │
│ (App) │
└──────┬──────┘
 │
 │ 1. api.units.list()
 ▼
┌──────────────────────────┐
│ @carf/geoapi-client │
│ │
│ 2. Interceptor Request │
│ ↓ │
│ 3. authClient.getToken()│
└──────┬───────────────────┘
 │
 │ 4. Token válido? (cache)
 ▼
┌──────────────────────────┐
│ @carf/tscore │
│ KeycloakClient │
│ │
│ SIM: Retorna cached │
│ NÃO: Refresh token │
└──────┬───────────────────┘
 │
 │ 5. Refresh token válido?
 ▼
┌──────────────────────────┐
│ Keycloak │
│ │
│ SIM: Retorna novo token │
│ NÃO: 401 Unauthorized │
└──────┬───────────────────┘
 │
 │ 6. Authorization: Bearer {token}
 ▼
┌──────────────────────────┐
│ GEOAPI │
│ (Backend .NET) │
│ │
│ - Valida JWT │
│ - Extrai claims │
│ - Verifica permissions │
│ - Retorna dados │
└──────────────────────────┘
```

## Configuração Inicial

### Instanciar Cliente

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'

// 1. Criar cliente Keycloak
const keycloakClient = new KeycloakClient({
 url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
 realm: 'carf',
 clientId: 'geoweb-client',
})

// 2. Criar cliente GEOAPI com auth
const apiClient = new GeoApiClient({
 baseURL: process.env.NEXT_PUBLIC_API_URL!,
 auth: keycloakClient,
})

// 3. Fazer login (redireciona para Keycloak)
await keycloakClient.login()

// 4. Após redirect, tokens estão disponíveis
const isAuthenticated = keycloakClient.isAuthenticated()
```

## Request Interceptor

```typescript
class GeoApiClient {
 private axiosInstance: AxiosInstance

 constructor(config: GeoApiClientConfig) {
 this.axiosInstance = axios.create({
 baseURL: config.baseURL,
 timeout: 30000,
 })

 // Interceptor que adiciona token
 this.axiosInstance.interceptors.request.use(
 async (config) => {
 if (!this.authClient) return config

 try {
 // Busca token (cached ou refreshed)
 const token = await this.authClient.getAccessToken()

 // Adiciona header Authorization
 config.headers.Authorization = `Bearer ${token}`

 return config
 } catch (error) {
 // Se falhar ao obter token, emite evento
 this.emit('auth:session-expired')
 throw error
 }
 },
 (error) => Promise.reject(error)
 )
 }
}
```

## Response Interceptor (401 Handling)

```typescript
this.axiosInstance.interceptors.response.use(
 (response) => response,
 async (error: AxiosError) => {
 const originalRequest = error.config as AxiosRequestConfig & {
 _retry?: boolean
 }

 // Se erro 401 e ainda não tentou retry
 if (error.response?.status === 401 && !originalRequest._retry) {
 originalRequest._retry = true

 try {
 // Tenta refresh token
 const newToken = await this.authClient.refreshAccessToken()

 // Atualiza header com novo token
 originalRequest.headers!.Authorization = `Bearer ${newToken}`

 // Retry request original
 return this.axiosInstance.request(originalRequest)
 } catch (refreshError) {
 // Refresh falhou - sessão expirou
 this.emit('auth:session-expired')
 throw refreshError
 }
 }

 // Se 403, não retry (sem permissão)
 if (error.response?.status === 403) {
 throw new ApiError(
 403,
 'FORBIDDEN',
 'Você não tem permissão para acessar este recurso'
 )
 }

 throw error
 }
)
```

## Token Management (via @carf/tscore)

### KeycloakClient Interface

```typescript
interface IAuthClient {
 /**
 * Retorna access token:
 * - Se válido e não expirado: retorna cached
 * - Se expirado mas refresh_token válido: faz refresh
 * - Se refresh_token expirado: throw error
 */
 getAccessToken(): Promise<string>

 /**
 * Força refresh do access token usando refresh_token
 */
 refreshAccessToken(): Promise<string>

 /**
 * Verifica se usuário está autenticado
 */
 isAuthenticated(): boolean

 /**
 * Faz logout (invalida sessão no Keycloak e limpa storage)
 */
 logout(): Promise<void>

 /**
 * Redireciona para página de login do Keycloak
 */
 login(): Promise<void>
}
```

### Token Storage

```typescript
// @carf/tscore armazena tokens em localStorage (web) ou SecureStore (mobile)

// Web (localStorage)
localStorage.setItem('access_token', token)
localStorage.setItem('refresh_token', refreshToken)
localStorage.setItem('expires_at', expiresAt)

// Mobile (React Native SecureStore)
await SecureStore.setItemAsync('access_token', token)
```

### Token Validation

```typescript
class KeycloakClient {
 async getAccessToken(): Promise<string> {
 const token = this.storage.getItem('access_token')
 const expiresAt = this.storage.getItem('expires_at')

 // Não tem token
 if (!token || !expiresAt) {
 throw new Error('No access token available')
 }

 // Token ainda válido (com margem de 5 minutos)
 const now = Date.now()
 const expiresAtTimestamp = parseInt(expiresAt, 10)
 const bufferMs = 5 * 60 * 1000 // 5 minutos

 if (now < expiresAtTimestamp - bufferMs) {
 return token // Retorna cached
 }

 // Token expirado ou perto de expirar - faz refresh
 return this.refreshAccessToken()
 }

 async refreshAccessToken(): Promise<string> {
 const refreshToken = this.storage.getItem('refresh_token')

 if (!refreshToken) {
 throw new Error('No refresh token available')
 }

 try {
 const response = await axios.post(
 `${this.config.url}/realms/${this.config.realm}/protocol/openid-connect/token`,
 new URLSearchParams({
 grant_type: 'refresh_token',
 refresh_token: refreshToken,
 client_id: this.config.clientId,
 }),
 {
 headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
 }
 )

 const { access_token, refresh_token, expires_in } = response.data

 // Armazena novos tokens
 this.storage.setItem('access_token', access_token)
 this.storage.setItem('refresh_token', refresh_token)
 this.storage.setItem(
 'expires_at',
 (Date.now() + expires_in * 1000).toString()
 )

 return access_token
 } catch (error) {
 // Refresh token inválido ou expirado
 this.clearTokens()
 throw new Error('Failed to refresh access token')
 }
 }
}
```

## Tratamento no App Consumidor

### React Context

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'
import { createContext, useContext, useEffect, useState } from 'react'

const ApiContext = createContext<GeoApiClient | null>(null)

export function ApiProvider({ children }: { children: React.ReactNode }) {
 const [apiClient, setApiClient] = useState<GeoApiClient | null>(null)

 useEffect(() => {
 const keycloak = new KeycloakClient({ /* ... */ })
 const client = new GeoApiClient({ auth: keycloak })

 // Escutar evento de sessão expirada
 client.on('auth:session-expired', () => {
 console.warn('Session expired, redirecting to login')
 keycloak.login()
 })

 setApiClient(client)
 }, [])

 return <ApiContext.Provider value={apiClient}>{children}</ApiContext.Provider>
}

export function useApi() {
 const client = useContext(ApiContext)
 if (!client) throw new Error('useApi must be used within ApiProvider')
 return client
}
```

### Uso em Componente

```typescript
function UnitsPage() {
 const api = useApi()

 const { data, error } = useQuery({
 queryKey: ['units'],
 queryFn: async () => {
 // Token automaticamente adicionado pelo interceptor
 const units = await api.units.list()
 return units
 },
 })

 // Se sessão expirar durante a query:
 // 1. Interceptor tenta refresh
 // 2. Se refresh falha, emite 'auth:session-expired'
 // 3. ApiProvider escuta e redireciona para login

 return <div>{/* render data */}</div>
}
```

## Logout

```typescript
async function handleLogout() {
 // 1. Invalida sessão no Keycloak
 await keycloakClient.logout()

 // 2. Limpa tokens do storage
 // (já feito pelo logout() acima)

 // 3. Redireciona para página de login
 router.push('/login')
}
```

## Refresh Token Rotation

Keycloak por padrão faz **refresh token rotation** - cada vez que você usa um refresh_token, recebe um novo refresh_token:

```
Request 1:
 refresh_token: abc123
 ↓
Response 1:
 access_token: xyz789
 refresh_token: def456 ← NOVO refresh_token

Request 2:
 refresh_token: def456 ← Usar o NOVO
 ↓
Response 2:
 access_token: uvw101
 refresh_token: ghi112 ← NOVO refresh_token
```

**Importante:** Sempre armazene o refresh_token retornado.

## Segurança

### PKCE (Proof Key for Code Exchange)

[PKCE](https://oauth.net/2/pkce/) é usado em public clients (GEOWEB, REURBCAD) para prevenir ataques de interceptação, implementado via [Keycloak JavaScript Adapter](https://www.keycloak.org/docs/latest/securing_apps/#_javascript_adapter):

```typescript
// 1. Gerar code_verifier (random string)
const codeVerifier = generateRandomString(128)

// 2. Gerar code_challenge (SHA256 hash)
const codeChallenge = await sha256(codeVerifier)

// 3. Incluir no authorization request
window.location.href = `${keycloakUrl}/auth?
 client_id=geoweb-client&
 redirect_uri=http://localhost:3000/callback&
 response_type=code&
 code_challenge=${codeChallenge}&
 code_challenge_method=S256`

// 4. Trocar code por token incluindo code_verifier
const tokens = await axios.post('/token', {
 code,
 code_verifier: codeVerifier,
})
```

### HTTPS Only

```typescript
// Em produção, SEMPRE usar HTTPS
if (process.env.NODE_ENV === 'production' && !config.baseURL.startsWith('https://')) {
 throw new Error('API URL must use HTTPS in production')
}
```
