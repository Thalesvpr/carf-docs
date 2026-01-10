# Arquitetura do Cliente GEOAPI

## Visão Geral

O **@carf/geoapi-client** é construído seguindo os princípios de **Clean Architecture** e **Separation of Concerns**, fornecendo uma camada de abstração sobre a comunicação HTTP com a API GEOAPI.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Consumer Application                      │
│              (GEOWEB, REURBCAD, ADMIN, etc)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ import { GeoApiClient }
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      GeoApiClient                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  units: UnitsApi                                     │   │
│  │  holders: HoldersApi                                 │   │
│  │  communities: CommunitiesApi                         │   │
│  │  legitimation: LegitimationApi                       │   │
│  │  reports: ReportsApi                                 │   │
│  │  auth: AuthenticationApi                             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      HttpClient                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - request(config): Promise<T>                       │   │
│  │  - get<T>(url, config): Promise<T>                   │   │
│  │  - post<T>(url, data, config): Promise<T>            │   │
│  │  - put<T>(url, data, config): Promise<T>             │   │
│  │  - delete<T>(url, config): Promise<T>                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           │                           │
           ↓                           ↓
┌────────────────────┐      ┌────────────────────┐
│   Interceptors     │      │   Error Handler    │
│  - Auth Token      │      │  - ApiError        │
│  - Tenant ID       │      │  - NetworkError    │
│  - Retry Logic     │      │  - ValidationError │
│  - Logging         │      │  - AuthError       │
└────────────────────┘      └────────────────────┘
           │
           ↓
┌─────────────────────────────────────────────────────────────┐
│                      Axios / Fetch                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
                   ┌─────────┐
                   │ GEOAPI  │
                   │ Backend │
                   └─────────┘
```

## Camadas da Arquitetura

### 1. API Endpoints Layer

**Responsabilidade:** Expor métodos tipados para cada domínio da API.

**Componentes:**
- `UnitsApi` - Operações sobre unidades habitacionais
- `HoldersApi` - Operações sobre posseiros
- `CommunitiesApi` - Operações sobre comunidades
- `LegitimationApi` - Processos de legitimação
- `ReportsApi` - Geração de relatórios
- `AuthenticationApi` - Autenticação e autorização

**Exemplo:**
```typescript
// src/endpoints/units.ts
export class UnitsApi {
  constructor(private http: HttpClient) {}

  async list(params: ListUnitsParams): Promise<PaginatedResponse<Unit>> {
    return this.http.get<PaginatedResponse<Unit>>('/api/units', { params });
  }

  async getById(id: string): Promise<Unit> {
    return this.http.get<Unit>(`/api/units/${id}`);
  }

  async create(data: CreateUnitRequest): Promise<Unit> {
    return this.http.post<Unit>('/api/units', data);
  }

  async update(id: string, data: UpdateUnitRequest): Promise<Unit> {
    return this.http.put<Unit>(`/api/units/${id}`, data);
  }

  async delete(id: string): Promise<void> {
    return this.http.delete<void>(`/api/units/${id}`);
  }
}
```

### 2. HTTP Client Layer

**Responsabilidade:** Gerenciar requisições HTTP, interceptors e configuração base.

**Implementação:**
```typescript
// src/client/http-client.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { KeycloakClient } from '@carf/tscore/auth';

export class HttpClient {
  private axios: AxiosInstance;

  constructor(
    private baseURL: string,
    private auth: KeycloakClient,
    private tenantId?: string
  ) {
    this.axios = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - inject auth token
    this.axios.interceptors.request.use(
      async (config) => {
        const token = await this.auth.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        if (this.tenantId) {
          config.headers['X-Tenant-ID'] = this.tenantId;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired, try refresh
          await this.auth.refreshToken();
          // Retry original request
          return this.axios.request(error.config);
        }
        return Promise.reject(this.transformError(error));
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.axios.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.axios.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.axios.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.axios.delete<T>(url, config);
    return response.data;
  }

  private transformError(error: any): ApiError {
    // Transform axios error to our custom ApiError
    return new ApiError(error);
  }
}
```

### 3. Interceptors Layer

**Responsabilidade:** Interceptar e modificar requests/responses.

**Interceptors implementados:**
1. **AuthInterceptor** - Injeta token JWT automaticamente
2. **TenantInterceptor** - Injeta tenant ID no header
3. **RetryInterceptor** - Retry automático em falhas transientes
4. **LoggingInterceptor** - Logs de requisições (debug mode)
5. **CacheInterceptor** - Cache de requisições GET (opcional)

### 4. Error Handling Layer

**Responsabilidade:** Transformar erros HTTP em erros tipados.

**Hierarquia de erros:**
```typescript
// src/client/errors.ts
export class ApiError extends Error {
  constructor(
    public message: string,
    public statusCode: number,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class NetworkError extends ApiError {
  constructor(message: string) {
    super(message, 0, 'NETWORK_ERROR');
    this.name = 'NetworkError';
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, public errors: Record<string, string[]>) {
    super(message, 400, 'VALIDATION_ERROR', errors);
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends ApiError {
  constructor(message: string) {
    super(message, 401, 'AUTHENTICATION_ERROR');
    this.name = 'AuthenticationError';
  }
}

export class AuthorizationError extends ApiError {
  constructor(message: string) {
    super(message, 403, 'AUTHORIZATION_ERROR');
    this.name = 'AuthorizationError';
  }
}

export class NotFoundError extends ApiError {
  constructor(resource: string) {
    super(`${resource} não encontrado`, 404, 'NOT_FOUND_ERROR');
    this.name = 'NotFoundError';
  }
}

export class ConflictError extends ApiError {
  constructor(message: string) {
    super(message, 409, 'CONFLICT_ERROR');
    this.name = 'ConflictError';
  }
}

export class ServerError extends ApiError {
  constructor(message: string) {
    super(message, 500, 'SERVER_ERROR');
    this.name = 'ServerError';
  }
}
```

### 5. Types Layer

**Responsabilidade:** Tipos TypeScript para requests/responses.

**Organização:**
```
types/
├── common.ts          # Tipos comuns (Pagination, etc)
├── units.ts           # Unit, CreateUnitRequest, UpdateUnitRequest
├── holders.ts         # Holder, CreateHolderRequest, etc
├── communities.ts     # Community types
├── legitimation.ts    # Legitimation types
├── reports.ts         # Report types
└── errors.ts          # Error types
```

## Design Patterns Utilizados

### 1. Facade Pattern
`GeoApiClient` atua como facade, fornecendo interface única para todos os endpoints.

### 2. Builder Pattern
Configuração do cliente via builder:
```typescript
const client = new GeoApiClientBuilder()
  .withBaseURL('https://api.carf.gov.br')
  .withAuth(keycloakClient)
  .withTenant('tenant-123')
  .withRetry({ maxRetries: 3 })
  .withCache({ ttl: 300 })
  .build();
```

### 3. Chain of Responsibility (Interceptors)
Interceptors formam uma cadeia de processamento.

### 4. Strategy Pattern
Error handling strategy pode ser customizada:
```typescript
const client = new GeoApiClient({
  errorHandler: new CustomErrorHandler()
});
```

### 5. Singleton (opcional)
Cliente pode ser singleton para compartilhar configuração:
```typescript
export const apiClient = GeoApiClient.getInstance({...});
```

## Fluxo de Requisição

```
1. Application calls API method
   api.units.list({ page: 1 })

2. UnitsApi prepares request
   this.http.get('/api/units', { params: { page: 1 } })

3. HttpClient intercepts request
   - AuthInterceptor adds Bearer token
   - TenantInterceptor adds X-Tenant-ID header
   - LoggingInterceptor logs request (if debug)

4. Axios sends HTTP request
   GET https://api.carf.gov.br/api/units?page=1
   Headers: { Authorization: Bearer xxx, X-Tenant-ID: yyy }

5. Response received
   - Status 200: Return data
   - Status 401: Refresh token + retry
   - Status 4xx/5xx: Transform to ApiError

6. HttpClient intercepts response
   - RetryInterceptor (if transient error)
   - CacheInterceptor (if cacheable)

7. Data returned to application
   const units: PaginatedResponse<Unit> = ...
```

## Configuração

### Minimal Configuration
```typescript
const api = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br',
  auth: keycloakClient
});
```

### Full Configuration
```typescript
const api = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br',
  auth: keycloakClient,
  tenant: 'tenant-123',
  timeout: 30000,
  retry: {
    maxRetries: 3,
    retryDelay: 1000,
    retryCondition: (error) => error.statusCode >= 500
  },
  cache: {
    enabled: true,
    ttl: 300,
    maxSize: 100
  },
  logging: {
    enabled: true,
    logLevel: 'debug'
  },
  interceptors: {
    request: [customRequestInterceptor],
    response: [customResponseInterceptor]
  }
});
```

## Dependency Injection

O cliente suporta DI para facilitar testes:

```typescript
// Production
const api = new GeoApiClient({
  httpClient: new AxiosHttpClient(),
  auth: new KeycloakClient()
});

// Testing
const api = new GeoApiClient({
  httpClient: new MockHttpClient(),
  auth: new MockAuthClient()
});
```

## Versionamento da API

Suporte a múltiplas versões da API:

```typescript
const apiV1 = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br/v1'
});

const apiV2 = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br/v2'
});
```

## Extensibilidade

### Custom Endpoints
```typescript
class CustomApi {
  constructor(private http: HttpClient) {}

  async customMethod(): Promise<any> {
    return this.http.get('/api/custom');
  }
}

// Extend client
const api = new GeoApiClient({...});
api.custom = new CustomApi(api.httpClient);
```

### Custom Interceptors
```typescript
const customInterceptor: RequestInterceptor = async (config) => {
  config.headers['X-Custom-Header'] = 'value';
  return config;
};

const api = new GeoApiClient({
  interceptors: {
    request: [customInterceptor]
  }
});
```

## Referências

- [ADR-007: Bun Runtime](../../../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-007-bun-runtime-bundler.md)
- **ADR-011: TSCORE Library**
- [CENTRAL API Specification](../../../../../../CENTRAL/API/README.md)
- **GEOAPI Backend Docs**
- [Axios Documentation](https://axios-http.com/)
