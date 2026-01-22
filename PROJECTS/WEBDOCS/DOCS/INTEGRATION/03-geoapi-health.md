---
type: leaf
status: review
updated: 2026-01-21
---

# Integração com GEOAPI Health

Status page do WEBDOCS consome endpoints /health dos serviços CARF para exibir disponibilidade em tempo real. Integração via fetch server-side durante SSR garante que informações são atuais sem expor URLs internas ao cliente.

Endpoint /health da GEOAPI retorna JSON com status (healthy, degraded, unhealthy), checks individuais (database, keycloak, minio), e timestamp. Response inclui latência de cada dependência permitindo identificar gargalos específicos.

Componente StatusPage.astro executa fetch para cada serviço configurado em src/config/services.ts durante renderização server-side. Timeout de 5 segundos previne que serviço lento bloqueie renderização. Serviços que não respondem são marcados como unknown com mensagem explicativa.

Serviços monitorados incluem GEOAPI verificando endpoint /health que testa conexão PostgreSQL e dependências, Keycloak verificando /.well-known/openid-configuration indicando que realm está operacional, e MinIO verificando endpoint /minio/health/live para storage de arquivos.

Client-side polling opcional via script que executa fetch a cada 30 segundos atualizando indicadores visuais sem reload da página. Polling desabilitado por padrão para economizar recursos, habilitado quando usuário clica em "atualização automática".

## Formato de Resposta GEOAPI /health

```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T15:30:00Z",
  "version": "1.2.3",
  "uptime": "5d 3h 22m",
  "checks": {
    "database": {
      "status": "healthy",
      "latency": 12,
      "details": {
        "connections": 15,
        "maxConnections": 100,
        "pendingQueries": 0
      }
    },
    "keycloak": {
      "status": "healthy",
      "latency": 45,
      "details": {
        "realm": "carf",
        "tokenEndpoint": "reachable"
      }
    },
    "minio": {
      "status": "healthy",
      "latency": 8,
      "details": {
        "bucket": "carf-documents",
        "availableSpace": "450GB"
      }
    },
    "redis": {
      "status": "degraded",
      "latency": 150,
      "details": {
        "message": "High latency detected",
        "memoryUsage": "85%"
      }
    }
  }
}
```

## Status Possíveis

| Status | Descrição | Cor |
|--------|-----------|-----|
| `healthy` | Serviço operando normalmente | Verde |
| `degraded` | Operando com problemas | Amarelo |
| `unhealthy` | Serviço indisponível | Vermelho |
| `unknown` | Não foi possível verificar | Cinza |

## Componente StatusGrid.astro

```astro
---
// src/components/StatusGrid.astro
import type { Service } from '../config/services';

interface Props {
  services: Service[];
  results: Map<string, HealthResult>;
}

interface HealthResult {
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  latency?: number;
  message?: string;
  checks?: Record<string, { status: string; latency: number }>;
}

const { services, results } = Astro.props;

const statusColors = {
  healthy: 'bg-green-500',
  degraded: 'bg-yellow-500',
  unhealthy: 'bg-red-500',
  unknown: 'bg-gray-400'
};

const statusLabels = {
  healthy: 'Operacional',
  degraded: 'Degradado',
  unhealthy: 'Indisponível',
  unknown: 'Desconhecido'
};
---

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {services.map((service) => {
    const result = results.get(service.id) ?? { status: 'unknown' };
    const colorClass = statusColors[result.status];
    const label = statusLabels[result.status];

    return (
      <div class="border rounded-lg p-4 bg-white dark:bg-gray-800">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold">{service.name}</h3>
          <span class={`${colorClass} text-white text-xs px-2 py-1 rounded`}>
            {label}
          </span>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {service.description}
        </p>
        {result.latency && (
          <p class="text-xs text-gray-500">
            Latência: {result.latency}ms
          </p>
        )}
        {result.message && (
          <p class="text-xs text-red-600 mt-1">{result.message}</p>
        )}
        {result.checks && (
          <div class="mt-3 pt-3 border-t">
            <p class="text-xs font-medium mb-1">Dependências:</p>
            {Object.entries(result.checks).map(([name, check]) => (
              <div class="flex justify-between text-xs">
                <span>{name}</span>
                <span class={check.status === 'healthy' ? 'text-green-600' : 'text-yellow-600'}>
                  {check.latency}ms
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  })}
</div>
```

## Serviço de Health Check

```typescript
// src/lib/health/service.ts
import { services, type Service } from '../../config/services';

export interface HealthResult {
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  latency?: number;
  message?: string;
  checks?: Record<string, { status: string; latency: number }>;
}

export async function checkService(service: Service): Promise<HealthResult> {
  if (!service.healthEndpoint) {
    return { status: 'unknown', message: 'No health endpoint configured' };
  }

  const start = Date.now();

  try {
    const response = await fetch(service.healthEndpoint, {
      signal: AbortSignal.timeout(service.timeout),
      headers: service.headers ?? {}
    });

    const latency = Date.now() - start;

    if (!response.ok) {
      return { status: 'unhealthy', latency, message: `HTTP ${response.status}` };
    }

    const data = await response.json().catch(() => null);

    // Verifica expected response se configurado
    if (service.expectedResponse?.bodyContains) {
      const text = JSON.stringify(data);
      if (!text.includes(service.expectedResponse.bodyContains)) {
        return { status: 'degraded', latency, message: 'Unexpected response' };
      }
    }

    return {
      status: data?.status ?? 'healthy',
      latency,
      checks: data?.checks
    };
  } catch (error) {
    const latency = Date.now() - start;
    const message = error instanceof Error ? error.message : 'Unknown error';
    return { status: 'unhealthy', latency, message };
  }
}

export async function checkAllServices(): Promise<Map<string, HealthResult>> {
  const results = new Map<string, HealthResult>();

  await Promise.all(
    services.map(async (service) => {
      const result = await checkService(service);
      results.set(service.id, result);
    })
  );

  return results;
}
```

## Página de Status

```astro
---
// src/pages/status.astro
import Layout from '../layouts/Layout.astro';
import StatusGrid from '../components/StatusGrid.astro';
import { services } from '../config/services';
import { checkAllServices } from '../lib/health/service';

// SSR: verifica status em cada request
const results = await checkAllServices();

// Calcula status geral
const allHealthy = [...results.values()].every(r => r.status === 'healthy');
const anyUnhealthy = [...results.values()].some(r => r.status === 'unhealthy');
const overallStatus = anyUnhealthy ? 'unhealthy' : allHealthy ? 'healthy' : 'degraded';
---

<Layout title="Status dos Serviços">
  <main class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-2">Status dos Serviços</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-6">
      Última verificação: {new Date().toLocaleString('pt-BR')}
    </p>

    <div class="mb-8 p-4 rounded-lg border-2 {overallStatus === 'healthy' ? 'border-green-500 bg-green-50' : overallStatus === 'degraded' ? 'border-yellow-500 bg-yellow-50' : 'border-red-500 bg-red-50'}">
      <p class="font-semibold">
        {overallStatus === 'healthy' ? '✅ Todos os sistemas operacionais' :
         overallStatus === 'degraded' ? '⚠️ Alguns serviços com problemas' :
         '🚨 Serviços indisponíveis'}
      </p>
    </div>

    <StatusGrid services={services} results={results} />
  </main>
</Layout>
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
