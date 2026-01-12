# HTTP Client - Cliente HTTP Base

## Visão Geral

O @carf/geoapi-client é construído sobre um cliente HTTP robusto que encapsula toda a comunicação com a GEOAPI backend. Fornece autenticação automática, tratamento de erros tipados, retry logic e suporte a interceptors customizados.

## Documentação de Referência

📖 **** - Especificação completa da REST API GEOAPI

📖 **** - Autenticação OAuth2/OIDC

📖 ****GEOAPI Backend Docs**** - Documentação do backend .NET

## Arquitetura do Cliente HTTP

```
┌─────────────────────────────────────────────────────────────┐
│ GeoApiClient │
│ (Main Entry Point) │
└───────────────┬─────────────────────────────────────────────┘
 │
 │ Composto por APIs específicas
 ├──────────────────────────────────────────────┐
 │ │
 ┌──────────▼──────┐ ┌──────────────┐ ┌───────────────┐
 │ UnitsApi │ │ HoldersApi │ │CommunitiesApi│
 │ (CRUD Units) │ │ (CRUD Holders)│ │ (CRUD Comms) │
 └────────┬────────┘ └──────┬───────┘ └───────┬───────┘
 │ │ │
 │ Todos usam o HttpClient base │
 └──────────────────┼───────────────────┘
 │
 ┌───────────▼────────────┐
 │ HttpClient Base │
 │ (Axios Wrapper) │
 └───────────┬────────────┘
 │
 ┌────────────────────────┼────────────────────────┐
 │ │ │
 ┌────▼─────┐ ┌───────▼──────┐ ┌────────▼────────┐
 │Request │ │ Response │ │ Error │
 │Interceptor│ │ Interceptor │ │ Handler │
 │ (Auth) │ │ (Transform) │ │ (Typed Errors) │
 └──────────┘ └──────────────┘ └─────────────────┘
```

## HttpClient Base

### Configuração

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'

// 1. Configurar autenticação
const auth = new KeycloakClient({
 url: 'https://keycloak.carf.gov.br',
 realm: 'carf',
 clientId: 'geoweb-client'
})

await auth.init()

// 2. Criar cliente API
const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 timeout: 30000, // 30 segundos
 retryAttempts: 3, // Retry em falhas transientes
 retryDelay: 1000, // 1 segundo entre retries
 enableLogging: true, // Logs de debug
})
```

### Opções de Configuração

```typescript
interface GeoApiClientConfig {
 // Required
 baseURL: string // URL base da API (ex: https://api.carf.gov.br)
 auth: KeycloakClient // Cliente Keycloak para autenticação

 // Optional - Timeouts
 timeout?: number // Timeout global (padrão: 30000ms)
 requestTimeout?: number // Timeout de request (padrão: usa global)
 uploadTimeout?: number // Timeout de upload (padrão: 300000ms = 5min)

 // Optional - Retry
 retryAttempts?: number // Tentativas de retry (padrão: 3)
 retryDelay?: number // Delay entre retries em ms (padrão: 1000)
 retryCondition?: (error) => boolean // Condição customizada para retry

 // Optional - Logging
 enableLogging?: boolean // Habilita logs (padrão: false)
 logger?: Logger // Logger customizado

 // Optional - Interceptors
 requestInterceptors?: RequestInterceptor[]
 responseInterceptors?: ResponseInterceptor[]

 // Optional - Headers
 defaultHeaders?: Record<string, string> // Headers padrão adicionais
}
```

## Request Interceptors

Interceptors de request modificam requests antes de serem enviados.

### Interceptor de Autenticação (Built-in)

Injeta automaticamente o JWT token no header `Authorization`.

```typescript
// Interno - automático quando `auth` é fornecido
async function authInterceptor(config: RequestConfig): Promise<RequestConfig> {
 const token = await auth.getToken()

 if (token) {
 config.headers = {
 ...config.headers,
 'Authorization': `Bearer ${token}`
 }
 }

 return config
}
```

📖 ****CENTRAL/SECURITY/01-authentication.md**** - Arquitetura de autenticação

### Interceptor de Tenant (Built-in)

Adiciona header `X-Tenant-Id` para multi-tenancy.

```typescript
// Interno - automático
async function tenantInterceptor(config: RequestConfig): Promise<RequestConfig> {
 const tenantId = await auth.getCurrentTenantId()

 if (tenantId) {
 config.headers = {
 ...config.headers,
 'X-Tenant-Id': tenantId
 }
 }

 return config
}
```

📖 ****CENTRAL/ARCHITECTURE/MULTI-TENANCY/01-overview.md**** - Multi-tenancy

### Custom Request Interceptor

```typescript
import { GeoApiClient, RequestInterceptor } from '@carf/geoapi-client'

// Criar interceptor customizado
const loggingInterceptor: RequestInterceptor = async (config) => {
 console.log(`[Request] ${config.method} ${config.url}`)
 return config
}

// Adicionar ao cliente
const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 requestInterceptors: [loggingInterceptor]
})
```

## Response Interceptors

Interceptors de response processam respostas antes de retornarem para o código.

### Interceptor de Transformação (Built-in)

Transforma datas ISO strings em objetos `Date`.

```typescript
// Interno - automático
function dateTransformInterceptor(response: Response): Response {
 function transformDates(obj: any): any {
 if (obj === null || typeof obj !== 'object') return obj

 // Detecta ISO date strings e converte
 if (typeof obj === 'string' && /^\d{4}-\d{2}-\d{2}T/.test(obj)) {
 return new Date(obj)
 }

 // Recursivo para objetos e arrays
 if (Array.isArray(obj)) {
 return obj.map(transformDates)
 }

 const transformed: any = {}
 for (const key in obj) {
 transformed[key] = transformDates(obj[key])
 }
 return transformed
 }

 response.data = transformDates(response.data)
 return response
}
```

### Custom Response Interceptor

```typescript
import { ResponseInterceptor } from '@carf/geoapi-client'

// Interceptor que extrai metadados de paginação
const paginationInterceptor: ResponseInterceptor = async (response) => {
 if (response.headers['x-total-count']) {
 response.data.pagination = {
 total: parseInt(response.headers['x-total-count'], 10),
 page: parseInt(response.headers['x-page'], 10),
 limit: parseInt(response.headers['x-limit'], 10)
 }
 }
 return response
}

const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 responseInterceptors: [paginationInterceptor]
})
```

## Error Handling

O cliente HTTP fornece erros tipados para tratamento específico.

### Hierarquia de Erros

```typescript
ApiError (base)
 ├── NetworkError (sem conectividade)
 ├── TimeoutError (timeout excedido)
 ├── ValidationError (400 - validação falhou)
 ├── UnauthorizedError (401 - não autenticado)
 ├── ForbiddenError (403 - sem permissão)
 ├── NotFoundError (404 - recurso não existe)
 ├── ConflictError (409 - conflito, ex: duplicate key)
 ├── UnprocessableEntityError (422 - erro semântico)
 ├── TooManyRequestsError (429 - rate limit)
 ├── InternalServerError (500 - erro do servidor)
 └── ServiceUnavailableError (503 - serviço indisponível)
```

📖 ****API Reference: Error Handling**** - Detalhes completos de cada erro

### Tratando Erros

```typescript
import {
 ValidationError,
 UnauthorizedError,
 NotFoundError,
 ConflictError
} from '@carf/geoapi-client'

try {
 const unit = await api.units.create(data)
} catch (error) {
 if (error instanceof ValidationError) {
 // 400 - Dados inválidos
 console.error('Validation errors:', error.validationErrors)
 // Mostrar erros no formulário
 } else if (error instanceof UnauthorizedError) {
 // 401 - Token expirado
 await auth.refreshToken()
 // Retry request
 } else if (error instanceof NotFoundError) {
 // 404 - Unidade não existe
 console.error('Unit not found')
 } else if (error instanceof ConflictError) {
 // 409 - CPF duplicado, código duplicado, etc.
 console.error('Conflict:', error.message)
 } else {
 // Erro desconhecido
 console.error('Unexpected error:', error)
 }
}
```

### ValidationError Details

Erros de validação (400) incluem detalhes estruturados:

```typescript
interface ValidationError extends ApiError {
 statusCode: 400
 validationErrors: {
 [field: string]: string[]
 }
}

// Exemplo de erro
{
 message: 'Validation failed',
 statusCode: 400,
 validationErrors: {
 'cpf': ['CPF inválido', 'CPF já cadastrado'],
 'email': ['Email obrigatório'],
 'code': ['Código já existe na comunidade']
 }
}
```

📖 ****CENTRAL/API/02-error-responses.md**** - Formato de respostas de erro

## Retry Logic

O cliente retenta automaticamente em falhas transientes.

### Condições de Retry

Por padrão, retry ocorre em:
- **Erros de rede** (NetworkError)
- **Timeout** (TimeoutError)
- **429 Too Many Requests** (rate limit)
- **500 Internal Server Error**
- **503 Service Unavailable**

### Configuração de Retry

```typescript
const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 retryAttempts: 3, // Máx 3 tentativas
 retryDelay: 1000, // 1 segundo entre tentativas
 retryCondition: (error) => {
 // Retry customizado
 return (
 error.statusCode === 503 ||
 error instanceof NetworkError ||
 error instanceof TimeoutError
 )
 }
})
```

### Exponential Backoff

```typescript
// Delay exponencial: 1s, 2s, 4s, 8s, ...
const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 retryAttempts: 4,
 retryDelay: (attemptNumber) => {
 return Math.pow(2, attemptNumber) * 1000
 }
})
```

## Request Cancellation

Suporta cancelamento de requests em andamento.

```typescript
import { CancelToken } from '@carf/geoapi-client'

// Criar cancel token
const cancelToken = CancelToken.source()

// Request com cancel token
const promise = api.units.list({ page: 1 }, { cancelToken: cancelToken.token })

// Cancelar depois de 5 segundos
setTimeout(() => {
 cancelToken.cancel('Request cancelled by user')
}, 5000)

try {
 const units = await promise
} catch (error) {
 if (CancelToken.isCancel(error)) {
 console.log('Request was cancelled:', error.message)
 }
}
```

### Uso com React

```typescript
import { useEffect, useState } from 'react'
import { GeoApiClient, CancelToken } from '@carf/geoapi-client'

function UnitsListComponent() {
 const [units, setUnits] = useState([])

 useEffect(() => {
 const cancelToken = CancelToken.source()

 api.units.list({ page: 1 }, { cancelToken: cancelToken.token })
 .then(setUnits)
 .catch(error => {
 if (!CancelToken.isCancel(error)) {
 console.error(error)
 }
 })

 // Cleanup: cancela request se componente desmontar
 return () => cancelToken.cancel()
 }, [])

 return <div>{/* Render units */}</div>
}
```

## Upload de Arquivos

Suporte a upload de arquivos com progress tracking.

```typescript
// Upload de imagem
const formData = new FormData()
formData.append('file', imageFile)
formData.append('type', 'PHOTO_FRONT')
formData.append('entityId', unitId)
formData.append('entityType', 'UNIT')

const document = await api.documents.upload(formData, {
 onUploadProgress: (progressEvent) => {
 const percentCompleted = Math.round(
 (progressEvent.loaded * 100) / progressEvent.total
 )
 console.log(`Upload: ${percentCompleted}%`)
 }
})
```

📖 ****HOW-TO: Upload de Arquivos**** - Guia completo

## Download de Arquivos

Suporte a download de arquivos grandes com streaming.

```typescript
// Download de relatório PDF
const blob = await api.reports.download('report-123', {
 onDownloadProgress: (progressEvent) => {
 const percentCompleted = Math.round(
 (progressEvent.loaded * 100) / progressEvent.total
 )
 console.log(`Download: ${percentCompleted}%`)
 }
})

// Criar URL e fazer download no browser
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = 'relatorio.pdf'
link.click()
```

## Logging

Sistema de logging configurável para debug.

```typescript
// Habilitar logs
const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 enableLogging: true
})

// Logs automáticos:
// [GeoApiClient] Request: GET /api/units?page=1
// [GeoApiClient] Response: 200 OK (234ms)
// [GeoApiClient] Error: 404 Not Found - Unit not found
```

### Logger Customizado

```typescript
import { Logger } from '@carf/geoapi-client'

class CustomLogger implements Logger {
 debug(message: string, ...args: any[]) {
 console.log(`[DEBUG] ${message}`, ...args)
 }

 info(message: string, ...args: any[]) {
 console.log(`[INFO] ${message}`, ...args)
 }

 warn(message: string, ...args: any[]) {
 console.warn(`[WARN] ${message}`, ...args)
 }

 error(message: string, ...args: any[]) {
 console.error(`[ERROR] ${message}`, ...args)
 }
}

const api = new GeoApiClient({
 baseURL: 'https://api.carf.gov.br',
 auth: auth,
 logger: new CustomLogger()
})
```

## Links Relacionados

### Documentação CENTRAL

- 📖 - Especificação da REST API
- 📖 - Segurança e autenticação
- 📖 **CENTRAL/ARCHITECTURE/MULTI-TENANCY/** - Multi-tenancy

### Outras Seções

- 📖 **API Reference: Error Handling**
- 📖 **HOW-TO: Basic Usage**
- 📖 [ARCHITECTURE: Client Architecture](../ARCHITECTURE/01-client-architecture.md)

### Bibliotecas Relacionadas

- 🔧 @carf/tscore - Types e autenticação

---

**Última atualização:** 2026-01-09
