---
type: leaf
title: "Error Handling - @carf/geoapi-client"
status: review
updated: 2026-01-21
source: "PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/ARCHITECTURE/02-error-handling.md"
---

# Error Handling - Guia Pratico

Guia pratico para tratamento de erros ao usar @carf/geoapi-client.

## Hierarquia de Erros

```typescript
import {
  ApiError,           // Base - todos herdam
  ValidationError,    // 400 - Dados invalidos
  UnauthorizedError,  // 401 - Nao autenticado
  ForbiddenError,     // 403 - Sem permissao
  NotFoundError,      // 404 - Nao encontrado
  ConflictError,      // 409 - Conflito (duplicado, versao)
  TooManyRequestsError, // 429 - Rate limit
  ServerError,        // 5xx - Erro do servidor
  NetworkError,       // 0 - Sem conexao
  TimeoutError,       // Timeout excedido
} from '@carf/geoapi-client'
```

## Tratamento Basico

```typescript
try {
  const unit = await api.units.create(data)
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`Erro ${error.status}: ${error.message}`)
    console.error('Codigo:', error.code)
    console.error('Detalhes:', error.details)
  }
}
```

## Tratamento por Tipo

### ValidationError (400)

Erro de validacao com detalhes por campo.

```typescript
try {
  await api.units.create(data)
} catch (error) {
  if (error instanceof ValidationError) {
    // error.validationErrors: { [campo]: string[] }
    console.log(error.validationErrors)
    // { cpf: ['CPF invalido'], email: ['Email obrigatorio'] }

    // Exibir no formulario
    Object.entries(error.validationErrors).forEach(([field, messages]) => {
      setFieldError(field, messages.join(', '))
    })
  }
}
```

### UnauthorizedError (401)

Token expirado ou invalido.

```typescript
try {
  await api.units.list()
} catch (error) {
  if (error instanceof UnauthorizedError) {
    // Tentar refresh do token
    try {
      await auth.refreshToken()
      // Retry da requisicao
      return await api.units.list()
    } catch {
      // Refresh falhou - redirecionar para login
      router.push('/login')
    }
  }
}
```

### ForbiddenError (403)

Usuario sem permissao para a acao.

```typescript
try {
  await api.units.delete('unit-123')
} catch (error) {
  if (error instanceof ForbiddenError) {
    toast.error('Voce nao tem permissao para excluir esta unidade')
  }
}
```

### NotFoundError (404)

Recurso nao existe.

```typescript
try {
  const unit = await api.units.getById('unit-123')
} catch (error) {
  if (error instanceof NotFoundError) {
    toast.error('Unidade nao encontrada')
    router.push('/units')
  }
}
```

### ConflictError (409)

Conflito de dados (duplicado ou versao).

```typescript
try {
  await api.units.update('unit-123', data)
} catch (error) {
  if (error instanceof ConflictError) {
    if (error.code === 'VERSION_CONFLICT') {
      // Outro usuario modificou
      toast.error('Dados foram alterados por outro usuario. Atualize a pagina.')
    } else if (error.code === 'DUPLICATE_CODE') {
      // Codigo duplicado
      setFieldError('code', 'Este codigo ja existe')
    }
  }
}
```

### TooManyRequestsError (429)

Rate limit atingido.

```typescript
try {
  await api.units.list()
} catch (error) {
  if (error instanceof TooManyRequestsError) {
    const retryAfter = error.retryAfter  // Segundos para aguardar
    toast.warning(`Muitas requisicoes. Aguarde ${retryAfter} segundos.`)

    // Retry automatico apos tempo indicado
    await sleep(retryAfter * 1000)
    return await api.units.list()
  }
}
```

### ServerError (5xx)

Erro interno do servidor.

```typescript
try {
  await api.units.create(data)
} catch (error) {
  if (error instanceof ServerError) {
    toast.error('Erro no servidor. Tente novamente em alguns minutos.')

    // Log para debugging
    console.error('Server error:', {
      status: error.status,
      message: error.message,
      requestId: error.requestId  // Para suporte
    })
  }
}
```

### NetworkError

Sem conexao com servidor.

```typescript
try {
  await api.units.list()
} catch (error) {
  if (error instanceof NetworkError) {
    toast.error('Sem conexao com o servidor. Verifique sua internet.')
  }
}
```

### TimeoutError

Requisicao excedeu timeout.

```typescript
try {
  await api.reports.exportUnits(filters, 'excel')
} catch (error) {
  if (error instanceof TimeoutError) {
    toast.error('Requisicao demorou muito. Tente novamente.')
  }
}
```

## Tratamento Centralizado

### Handler Global

```typescript
function handleApiError(error: unknown): void {
  if (!(error instanceof ApiError)) {
    console.error('Unexpected error:', error)
    toast.error('Erro inesperado')
    return
  }

  switch (true) {
    case error instanceof ValidationError:
      // Nao mostrar toast - exibir no formulario
      break

    case error instanceof UnauthorizedError:
      auth.logout()
      router.push('/login')
      break

    case error instanceof ForbiddenError:
      toast.error('Sem permissao para esta acao')
      break

    case error instanceof NotFoundError:
      toast.error('Recurso nao encontrado')
      break

    case error instanceof ConflictError:
      toast.error('Conflito de dados. Atualize a pagina.')
      break

    case error instanceof TooManyRequestsError:
      toast.warning('Muitas requisicoes. Aguarde um momento.')
      break

    case error instanceof ServerError:
      toast.error('Erro no servidor. Tente novamente.')
      break

    case error instanceof NetworkError:
      toast.error('Sem conexao')
      break

    default:
      toast.error(error.message)
  }
}
```

### React Error Boundary

```tsx
import { Component, ReactNode } from 'react'
import { ApiError, ServerError, NetworkError } from '@carf/geoapi-client'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ApiErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error) {
    if (error instanceof ApiError) {
      console.error('API Error:', {
        status: error.status,
        code: error.code,
        message: error.message,
        requestId: error.requestId
      })
    }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />
    }
    return this.props.children
  }
}
```

### React Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ApiError, UnauthorizedError } from '@carf/geoapi-client'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Nao retry em erros de cliente (4xx)
        if (error instanceof ApiError && error.status < 500) {
          return false
        }
        return failureCount < 3
      }
    },
    mutations: {
      onError: (error) => {
        if (error instanceof UnauthorizedError) {
          // Redirecionar para login
          window.location.href = '/login'
        }
      }
    }
  }
})
```

## Logging de Erros

```typescript
function logApiError(error: ApiError): void {
  const logData = {
    status: error.status,
    code: error.code,
    message: error.message,
    requestId: error.requestId,
    timestamp: new Date().toISOString(),
    url: window.location.href
  }

  // Console para dev
  console.error('API Error:', logData)

  // Enviar para servico de monitoramento (Sentry, etc)
  if (typeof Sentry !== 'undefined') {
    Sentry.captureException(error, {
      tags: {
        errorCode: error.code,
        statusCode: error.status.toString()
      },
      extra: logData
    })
  }
}
```

## Boas Praticas

### 1. Seja especifico

```typescript
// Ruim - trata todos os erros igual
catch (error) {
  toast.error('Ocorreu um erro')
}

// Bom - tratamento especifico
catch (error) {
  if (error instanceof ValidationError) {
    // Mostrar erros no formulario
  } else if (error instanceof NotFoundError) {
    // Redirecionar para listagem
  } else {
    // Erro generico
  }
}
```

### 2. Nao esconda erros

```typescript
// Ruim - silencia o erro
catch (error) {
  // nada
}

// Bom - pelo menos loga
catch (error) {
  console.error('Error:', error)
}
```

### 3. Use requestId para suporte

```typescript
catch (error) {
  if (error instanceof ApiError) {
    toast.error(`Erro: ${error.message}. Codigo: ${error.requestId}`)
    // Usuario pode informar requestId ao suporte
  }
}
```

### 4. Retry inteligente

```typescript
// Retry apenas em erros transientes
catch (error) {
  if (error instanceof ServerError || error instanceof NetworkError) {
    // Pode tentar novamente
    await retry(operation)
  } else {
    // Nao faz sentido retry
    throw error
  }
}
```
