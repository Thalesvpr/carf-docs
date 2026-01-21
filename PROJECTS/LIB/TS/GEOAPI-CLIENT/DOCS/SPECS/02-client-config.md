---
title: "Configuracao do Cliente - @carf/geoapi-client"
status: review
updated: 2026-01-21
source: "interno"
---

# Configuracao do Cliente - @carf/geoapi-client

Interface unificada e definitiva de configuracao do GeoApiClient.

## Interface de Configuracao

```typescript
interface GeoApiClientConfig {
  // ============================================
  // OBRIGATORIOS
  // ============================================

  /**
   * URL base da API
   * @example "https://api.carf.gov.br"
   * @example "http://localhost:5000" (desenvolvimento)
   */
  baseURL: string

  /**
   * Cliente de autenticacao Keycloak
   * Responsavel por fornecer tokens JWT
   */
  auth: KeycloakClient

  // ============================================
  // OPCIONAIS - Timeout
  // ============================================

  /**
   * Timeout global para todas as requisicoes em milliseconds
   * @default 30000 (30 segundos)
   */
  timeout?: number

  /**
   * Timeout especifico para uploads em milliseconds
   * @default 300000 (5 minutos)
   */
  uploadTimeout?: number

  /**
   * Timeout especifico para downloads em milliseconds
   * @default 300000 (5 minutos)
   */
  downloadTimeout?: number

  // ============================================
  // OPCIONAIS - Retry
  // ============================================

  /**
   * Numero maximo de tentativas de retry
   * @default 3
   */
  retryAttempts?: number

  /**
   * Delay base entre retries em milliseconds
   * Usa exponential backoff: delay * 2^attempt
   * @default 1000 (1 segundo)
   */
  retryDelay?: number

  /**
   * Funcao customizada para determinar se deve fazer retry
   * @default Retry em 5xx, 429, network errors
   */
  retryCondition?: (error: ApiError) => boolean

  // ============================================
  // OPCIONAIS - Circuit Breaker
  // ============================================

  /**
   * Habilitar circuit breaker
   * @default true
   */
  enableCircuitBreaker?: boolean

  /**
   * Numero de falhas consecutivas para abrir circuito
   * @default 5
   */
  circuitBreakerThreshold?: number

  /**
   * Tempo em ms que circuito fica aberto antes de tentar half-open
   * @default 30000 (30 segundos)
   */
  circuitBreakerTimeout?: number

  // ============================================
  // OPCIONAIS - Logging
  // ============================================

  /**
   * Habilitar logs de debug
   * @default false
   */
  enableLogging?: boolean

  /**
   * Logger customizado
   * @default console
   */
  logger?: Logger

  // ============================================
  // OPCIONAIS - Headers
  // ============================================

  /**
   * Headers customizados adicionados a todas as requisicoes
   */
  defaultHeaders?: Record<string, string>

  /**
   * Tenant ID para multi-tenancy
   * Se nao fornecido, tenta obter do auth client
   */
  tenantId?: string
}
```

## Interface do Logger

```typescript
interface Logger {
  debug(message: string, ...args: unknown[]): void
  info(message: string, ...args: unknown[]): void
  warn(message: string, ...args: unknown[]): void
  error(message: string, ...args: unknown[]): void
}
```

## Exemplos de Configuracao

### Configuracao Minima

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'

const auth = new KeycloakClient({
  url: 'https://keycloak.carf.gov.br',
  realm: 'carf',
  clientId: 'geoweb-client'
})

const api = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br',
  auth
})
```

### Configuracao Completa

```typescript
import { GeoApiClient, ApiError } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'

const auth = new KeycloakClient({
  url: process.env.KEYCLOAK_URL!,
  realm: 'carf',
  clientId: 'geoweb-client'
})

const api = new GeoApiClient({
  // Obrigatorios
  baseURL: process.env.API_URL!,
  auth,

  // Timeouts
  timeout: 30000,           // 30s para requisicoes normais
  uploadTimeout: 600000,    // 10min para uploads
  downloadTimeout: 300000,  // 5min para downloads

  // Retry
  retryAttempts: 3,
  retryDelay: 1000,
  retryCondition: (error: ApiError) => {
    // Retry em server errors e rate limit
    return error.status >= 500 || error.status === 429
  },

  // Circuit Breaker
  enableCircuitBreaker: true,
  circuitBreakerThreshold: 5,
  circuitBreakerTimeout: 30000,

  // Logging
  enableLogging: process.env.NODE_ENV === 'development',
  logger: console,

  // Headers
  defaultHeaders: {
    'X-Client-Version': '1.0.0',
    'X-Client-Name': 'GEOWEB'
  },

  // Tenant
  tenantId: 'municipio-sp-001'
})
```

### Configuracao para Desenvolvimento

```typescript
const api = new GeoApiClient({
  baseURL: 'http://localhost:5000',
  auth,

  // Timeouts mais curtos para dev
  timeout: 10000,

  // Sem retry para ver erros imediatamente
  retryAttempts: 0,

  // Logging habilitado
  enableLogging: true,

  // Circuit breaker desabilitado
  enableCircuitBreaker: false
})
```

### Configuracao para Producao

```typescript
const api = new GeoApiClient({
  baseURL: process.env.API_URL!,
  auth,

  // Timeouts generosos
  timeout: 30000,
  uploadTimeout: 600000,

  // Retry agressivo
  retryAttempts: 5,
  retryDelay: 2000,

  // Circuit breaker habilitado
  enableCircuitBreaker: true,
  circuitBreakerThreshold: 10,
  circuitBreakerTimeout: 60000,

  // Logging apenas erros
  enableLogging: false,
})
```

## Valores Padrao

| Opcao | Valor Padrao |
|:------|:-------------|
| timeout | 30000 |
| uploadTimeout | 300000 |
| downloadTimeout | 300000 |
| retryAttempts | 3 |
| retryDelay | 1000 |
| enableCircuitBreaker | true |
| circuitBreakerThreshold | 5 |
| circuitBreakerTimeout | 30000 |
| enableLogging | false |

## Validacao de Configuracao

O cliente valida configuracao na inicializacao:

```typescript
const api = new GeoApiClient({
  baseURL: '',  // Erro: baseURL e obrigatorio
  auth: null    // Erro: auth e obrigatorio
})
// Throws: ConfigurationError: baseURL is required
```

## Alterando Configuracao em Runtime

Algumas configuracoes podem ser alteradas apos inicializacao:

```typescript
// Alterar timeout
api.setConfig({ timeout: 60000 })

// Alterar tenant
api.setConfig({ tenantId: 'outro-tenant' })

// Habilitar logging
api.setConfig({ enableLogging: true })
```

**Atencao:** baseURL e auth NAO podem ser alterados apos inicializacao.

## Integracao com Frameworks

### Next.js

```typescript
// lib/api.ts
import { GeoApiClient } from '@carf/geoapi-client'
import { KeycloakClient } from '@carf/tscore/auth'

let apiClient: GeoApiClient | null = null

export function getApiClient(): GeoApiClient {
  if (!apiClient) {
    const auth = new KeycloakClient({
      url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
      realm: 'carf',
      clientId: 'geoweb-client'
    })

    apiClient = new GeoApiClient({
      baseURL: process.env.NEXT_PUBLIC_API_URL!,
      auth
    })
  }
  return apiClient
}
```

### React Context

```tsx
// contexts/ApiContext.tsx
import { createContext, useContext, useMemo } from 'react'
import { GeoApiClient } from '@carf/geoapi-client'
import { useAuth } from '@carf/tscore/auth/react'

const ApiContext = createContext<GeoApiClient | null>(null)

export function ApiProvider({ children }: { children: React.ReactNode }) {
  const { client: auth } = useAuth()

  const api = useMemo(() => {
    if (!auth) return null
    return new GeoApiClient({
      baseURL: process.env.REACT_APP_API_URL!,
      auth
    })
  }, [auth])

  return (
    <ApiContext.Provider value={api}>
      {children}
    </ApiContext.Provider>
  )
}

export function useApi(): GeoApiClient {
  const api = useContext(ApiContext)
  if (!api) throw new Error('useApi must be used within ApiProvider')
  return api
}
```
