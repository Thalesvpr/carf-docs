# Error Handling - @carf/geoapi-client

## Sistema de Tratamento de Erros

Error handling no @carf/geoapi-client implementa retry logic automático com exponential backoff para erros temporários (5xx, network errors) tentando até 3 vezes com delays de 1s, 2s, 4s usando [axios-retry](https://github.com/softonic/axios-retry), [circuit breaker pattern](https://martinfowler.com/bliki/CircuitBreaker.html) para prevenir cascading failures abrindo circuit após 5 falhas consecutivas e retornando erro imediato por 30s antes de tentar half-open state, e error types tipados via `ApiError` class com campos `status` (HTTP code), `code` (error code do backend como `UNIT_NOT_FOUND`), `message` (mensagem humanizada), `details` (objeto com campos extras), `timestamp`, e `requestId` para correlação de logs, aplicações consumidoras podem tratar erros com `try-catch` verificando `error instanceof ApiError` e exibindo mensagens apropriadas via toast notifications ou [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary).

## ApiError Class

```typescript
export class ApiError extends Error {
 constructor(
 public status: number,
 public code: string,
 message: string,
 public details?: Record<string, any>,
 public timestamp?: Date,
 public requestId?: string
 ) {
 super(message)
 this.name = 'ApiError'

 // Mantém stack trace no V8
 if (Error.captureStackTrace) {
 Error.captureStackTrace(this, ApiError)
 }
 }

 isClientError(): boolean {
 return this.status >= 400 && this.status < 500
 }

 isServerError(): boolean {
 return this.status >= 500
 }

 isNetworkError(): boolean {
 return this.status === 0 || this.code === 'NETWORK_ERROR'
 }
}
```

## Retry Logic

### Configuração Axios-Retry

```typescript
import axiosRetry from 'axios-retry'

const client = axios.create({
 baseURL: 'https://api.carf.gov.br',
 timeout: 30000,
})

axiosRetry(client, {
 retries: 3,
 retryDelay: axiosRetry.exponentialDelay,
 retryCondition: (error) => {
 // Retry em erros de network
 if (axiosRetry.isNetworkError(error)) return true

 // Retry em 5xx
 if (error.response?.status >= 500) return true

 // Retry em 429 (Rate Limit)
 if (error.response?.status === 429) return true

 // Não retry em 4xx (client errors)
 return false
 },
 onRetry: (retryCount, error, requestConfig) => {
 console.warn(`Retry attempt ${retryCount} for ${requestConfig.url}`, {
 error: error.message,
 status: error.response?.status,
 })
 },
})
```

### Exponential Backoff

```
Tentativa 1: Imediato
Tentativa 2: Aguarda 1 segundo
Tentativa 3: Aguarda 2 segundos
Tentativa 4: Aguarda 4 segundos
```

## Circuit Breaker

```typescript
class CircuitBreaker {
 private failureCount = 0
 private lastFailureTime?: Date
 private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED'

 constructor(
 private threshold = 5,
 private timeout = 30000 // 30s
 ) {}

 async execute<T>(fn: () => Promise<T>): Promise<T> {
 if (this.state === 'OPEN') {
 if (this.shouldAttemptReset()) {
 this.state = 'HALF_OPEN'
 } else {
 throw new ApiError(
 503,
 'CIRCUIT_OPEN',
 'Service temporarily unavailable. Circuit breaker is open.'
 )
 }
 }

 try {
 const result = await fn()
 this.onSuccess()
 return result
 } catch (error) {
 this.onFailure()
 throw error
 }
 }

 private onSuccess() {
 this.failureCount = 0
 this.state = 'CLOSED'
 }

 private onFailure() {
 this.failureCount++
 this.lastFailureTime = new Date()

 if (this.failureCount >= this.threshold) {
 this.state = 'OPEN'
 console.warn('Circuit breaker opened due to repeated failures')
 }
 }

 private shouldAttemptReset(): boolean {
 if (!this.lastFailureTime) return false

 const now = new Date().getTime()
 const lastFailure = this.lastFailureTime.getTime()

 return now - lastFailure >= this.timeout
 }
}

// Uso no client
const circuitBreaker = new CircuitBreaker()

async function fetchUnits() {
 return circuitBreaker.execute(() => {
 return axios.get('/api/units')
 })
}
```

## Error Interceptor

```typescript
client.interceptors.response.use(
 (response) => response,
 (error: AxiosError) => {
 // Network error
 if (!error.response) {
 throw new ApiError(
 0,
 'NETWORK_ERROR',
 'Não foi possível conectar ao servidor. Verifique sua conexão.',
 { originalError: error.message }
 )
 }

 const { status, data } = error.response

 // Parse error response do backend
 const errorData = data as {
 code?: string
 message?: string
 details?: Record<string, any>
 timestamp?: string
 requestId?: string
 }

 throw new ApiError(
 status,
 errorData.code || 'UNKNOWN_ERROR',
 errorData.message || error.message,
 errorData.details,
 errorData.timestamp ? new Date(errorData.timestamp) : new Date(),
 errorData.requestId
 )
 }
)
```

## Tratamento no Cliente

### Try-Catch Básico

```typescript
import { ApiError } from '@carf/geoapi-client'

async function loadUnits() {
 try {
 const units = await api.units.list()
 return units
 } catch (error) {
 if (error instanceof ApiError) {
 // Erro conhecido do backend
 console.error(`API Error [${error.code}]:`, error.message)

 if (error.status === 404) {
 toast.error('Unidades não encontradas')
 } else if (error.status === 403) {
 toast.error('Você não tem permissão para acessar as unidades')
 } else if (error.isServerError()) {
 toast.error('Erro no servidor. Tente novamente mais tarde.')
 }
 } else {
 // Erro inesperado
 console.error('Unexpected error:', error)
 toast.error('Erro inesperado. Contate o suporte.')
 }
 }
}
```

### Error Boundary (React)

```typescript
import { Component, ReactNode } from 'react'
import { ApiError } from '@carf/geoapi-client'

interface Props {
 children: ReactNode
}

interface State {
 hasError: boolean
 error?: ApiError
}

export class ApiErrorBoundary extends Component<Props, State> {
 constructor(props: Props) {
 super(props)
 this.state = { hasError: false }
 }

 static getDerivedStateFromError(error: Error): State {
 if (error instanceof ApiError) {
 return { hasError: true, error }
 }
 return { hasError: true }
 }

 componentDidCatch(error: Error) {
 if (error instanceof ApiError) {
 console.error('API Error caught by boundary:', {
 code: error.code,
 status: error.status,
 message: error.message,
 requestId: error.requestId,
 })
 }
 }

 render() {
 if (this.state.hasError) {
 const { error } = this.state

 if (error?.status === 403) {
 return <div>Você não tem permissão para acessar este recurso.</div>
 }

 if (error?.isServerError()) {
 return <div>Erro no servidor. Tente novamente mais tarde.</div>
 }

 return <div>Ocorreu um erro inesperado.</div>
 }

 return this.props.children
 }
}
```

### React Query Error Handler

```typescript
import { useQuery } from '@tanstack/react-query'
import { ApiError } from '@carf/geoapi-client'

function UnitsPage() {
 const { data, error, isLoading } = useQuery({
 queryKey: ['units'],
 queryFn: () => api.units.list(),
 retry: (failureCount, error) => {
 // Não retry em client errors (4xx)
 if (error instanceof ApiError && error.isClientError()) {
 return false
 }
 // Retry até 3 vezes em outros erros
 return failureCount < 3
 },
 })

 if (error instanceof ApiError) {
 if (error.status === 404) {
 return <div>Nenhuma unidade encontrada</div>
 }

 if (error.status === 403) {
 return <div>Sem permissão</div>
 }

 return <div>Erro: {error.message}</div>
 }

 // ...render data
}
```

## Códigos de Erro do Backend

### 4xx - Client Errors

| Código | Status | Descrição |
|--------|--------|-----------|
| `UNIT_NOT_FOUND` | 404 | Unidade não encontrada |
| `HOLDER_NOT_FOUND` | 404 | Posseiro não encontrado |
| `INVALID_CPF` | 400 | CPF inválido |
| `INVALID_COORDINATES` | 400 | Coordenadas geográficas inválidas |
| `UNIT_CODE_DUPLICATE` | 409 | Código de unidade já existe |
| `UNAUTHORIZED` | 401 | Token de autenticação inválido ou expirado |
| `FORBIDDEN` | 403 | Usuário sem permissão para esta operação |
| `VALIDATION_ERROR` | 422 | Erro de validação (detalhes em `details`) |

### 5xx - Server Errors

| Código | Status | Descrição |
|--------|--------|-----------|
| `INTERNAL_ERROR` | 500 | Erro interno do servidor |
| `DATABASE_ERROR` | 500 | Erro ao acessar banco de dados |
| `SERVICE_UNAVAILABLE` | 503 | Serviço temporariamente indisponível |

### 0 - Network Errors

| Código | Status | Descrição |
|--------|--------|-----------|
| `NETWORK_ERROR` | 0 | Erro de conexão (sem resposta do servidor) |
| `TIMEOUT` | 0 | Request excedeu timeout de 30s |
| `CIRCUIT_OPEN` | 503 | Circuit breaker aberto |

## Logging de Erros

```typescript
function logError(error: ApiError) {
 // Em produção, enviar para Sentry, LogRocket, etc.
 console.error('API Error:', {
 code: error.code,
 status: error.status,
 message: error.message,
 details: error.details,
 requestId: error.requestId,
 timestamp: error.timestamp,
 stack: error.stack,
 })

 // Exemplo com Sentry
 if (typeof Sentry !== 'undefined') {
 Sentry.captureException(error, {
 tags: {
 errorCode: error.code,
 statusCode: error.status.toString(),
 },
 extra: {
 requestId: error.requestId,
 details: error.details,
 },
 })
 }
}
```
