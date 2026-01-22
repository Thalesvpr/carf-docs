---
type: leaf
status: review
updated: 2026-01-21
---

# Status Page

Página /status/ exibe disponibilidade em tempo real dos serviços CARF permitindo usuários verificarem se sistema está operacional antes de reportar problemas. Implementação combina checks server-side durante SSR com polling opcional client-side.

Layout apresenta card para cada serviço com indicador visual de status (verde para healthy, amarelo para degraded, vermelho para unhealthy, cinza para unknown), nome do serviço, latência do último check, e timestamp da verificação. Seção inferior mostra histórico de incidentes recentes ordenados por data.

## Configuração de Serviços

Serviços monitorados são configurados em formato JSON permitindo adicionar novos serviços sem modificar componentes. Configuração usa variáveis de ambiente para URLs, permitindo valores distintos por ambiente.

```json
{
  "services": [
    {
      "id": "geoapi",
      "name": "GeoAPI",
      "description": "API principal do sistema CARF",
      "healthEndpoint": "${GEOAPI_HEALTH_URL}",
      "timeout": 5000,
      "critical": true,
      "expectedResponse": {
        "status": 200,
        "body": { "status": "healthy" }
      }
    },
    {
      "id": "keycloak",
      "name": "Autenticação",
      "description": "Servidor de identidade Keycloak",
      "healthEndpoint": "${KEYCLOAK_HEALTH_URL}",
      "timeout": 5000,
      "critical": true,
      "expectedResponse": {
        "status": 200,
        "body": "JSON com issuer"
      }
    },
    {
      "id": "minio",
      "name": "Armazenamento",
      "description": "Armazenamento de arquivos e documentos",
      "healthEndpoint": "${MINIO_HEALTH_URL}",
      "timeout": 5000,
      "critical": false,
      "expectedResponse": {
        "status": 200
      }
    },
    {
      "id": "postgres",
      "name": "Banco de Dados",
      "description": "PostgreSQL com PostGIS",
      "healthEndpoint": null,
      "checkVia": "geoapi",
      "critical": true,
      "note": "Verificado indiretamente via health da GeoAPI"
    }
  ]
}
```

## Configuração de Polling

```json
{
  "polling": {
    "interval": 30000,
    "retries": 2,
    "retryDelay": 1000,
    "enabled": true,
    "userToggle": true
  }
}
```

## Estados de Status

```json
{
  "states": {
    "online": {
      "condition": "Response 200 dentro do timeout",
      "color": "#22c55e",
      "icon": "check-circle",
      "label": "Operacional"
    },
    "degraded": {
      "condition": "Response 200 mas latência > 2000ms",
      "color": "#eab308",
      "icon": "alert-triangle",
      "label": "Degradado"
    },
    "offline": {
      "condition": "Response != 200 ou timeout",
      "color": "#ef4444",
      "icon": "x-circle",
      "label": "Indisponível"
    },
    "unknown": {
      "condition": "Erro de rede ou primeira verificação",
      "color": "#6b7280",
      "icon": "help-circle",
      "label": "Desconhecido"
    }
  }
}
```

Health check executa durante SSR garantindo que página carrega com dados atuais. Componente StatusGrid.astro itera sobre serviços configurados executando fetch paralelo com Promise.allSettled para não bloquear em caso de timeout. Resultados são passados para componentes visuais conforme SPECS/13-componentes.md.

Histórico de incidentes mantido em collection do Decap CMS permite equipe de operações documentar manutenções programadas e falhas passadas via interface visual. Frontmatter inclui data, serviços afetados, descrição, e status (investigating, identified, monitoring, resolved). Configuração da collection em SPECS/15-decap-cms-config.md.

Polling client-side habilitado via checkbox "atualização automática" executa fetch a cada 30 segundos atualizando indicadores sem reload. Implementado com setInterval e fetch para endpoint API interno /api/health que retorna JSON com status atual de todos serviços.

## Implementação TypeScript

### Interface de Serviço

```typescript
// src/config/services.ts
export interface Service {
  /** Identificador único do serviço */
  id: string;
  /** Nome para exibição */
  name: string;
  /** Descrição curta do serviço */
    /** URL do endpoint de health check (null se verificado via outro serviço) */
  healthEndpoint: string | null;
  /** Timeout em ms para o health check */
  timeout: number;
  /** Se true, falha deste serviço indica sistema indisponível */
  critical: boolean;
  /** Se healthEndpoint é null, indica qual serviço verifica este */
  checkVia?: string;
  /** Response esperada para considerar healthy */
  expectedResponse?: {
    status: number;
    body?: Record<string, unknown>;
  };
}

export interface HealthCheckResult {
  serviceId: string;
  status: 'online' | 'degraded' | 'offline' | 'unknown';
  latency: number | null;
  checkedAt: Date;
  error?: string;
}

export interface StatusPageData {
  results: HealthCheckResult[];
  overallStatus: 'operational' | 'degraded' | 'major_outage';
  lastUpdated: Date;
}
```

### Configuração de Serviços

```typescript
// src/config/services.ts
export const services: Service[] = [
  {
    id: 'geoapi',
    name: 'GeoAPI',
    description: 'API principal do sistema CARF',
    healthEndpoint: import.meta.env.GEOAPI_HEALTH_URL || 'https://api.carf.com.br/health',
    timeout: 5000,
    critical: true,
    expectedResponse: {
      status: 200,
      body: { status: 'healthy' }
    }
  },
  {
    id: 'keycloak',
    name: 'Autenticação',
    description: 'Servidor de identidade Keycloak',
    healthEndpoint: import.meta.env.KEYCLOAK_HEALTH_URL ||
      `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}/.well-known/openid-configuration`,
    timeout: 5000,
    critical: true,
    expectedResponse: {
      status: 200
    }
  },
  {
    id: 'minio',
    name: 'Armazenamento',
    description: 'Armazenamento de arquivos e documentos',
    healthEndpoint: import.meta.env.MINIO_HEALTH_URL || 'https://storage.carf.com.br/minio/health/live',
    timeout: 5000,
    critical: false,
    expectedResponse: {
      status: 200
    }
  },
  {
    id: 'postgres',
    name: 'Banco de Dados',
    description: 'PostgreSQL com PostGIS',
    healthEndpoint: null,
    checkVia: 'geoapi',
    timeout: 5000,
    critical: true
  }
];
```

### Função de Health Check

```typescript
// src/lib/health/checker.ts
import { services, type Service, type HealthCheckResult, type StatusPageData } from '../../config/services';

const DEGRADED_LATENCY_THRESHOLD = 2000;

async function checkService(service: Service): Promise<HealthCheckResult> {
  const checkedAt = new Date();

  // Serviço verificado via outro
  if (!service.healthEndpoint) {
    return {
      serviceId: service.id,
      status: 'unknown',
      latency: null,
      checkedAt,
      error: `Verificado via ${service.checkVia}`
    };
  }

  const startTime = performance.now();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), service.timeout);

    const response = await fetch(service.healthEndpoint, {
      signal: controller.signal,
      headers: { 'Accept': 'application/json' }
    });

    clearTimeout(timeoutId);

    const latency = Math.round(performance.now() - startTime);

    // Verificar status code
    if (response.status !== (service.expectedResponse?.status || 200)) {
      return {
        serviceId: service.id,
        status: 'offline',
        latency,
        checkedAt,
        error: `Status ${response.status}`
      };
    }

    // Verificar body se especificado
    if (service.expectedResponse?.body) {
      const body = await response.json();
      const expectedKeys = Object.keys(service.expectedResponse.body);

      for (const key of expectedKeys) {
        if (body[key] !== service.expectedResponse.body[key]) {
          return {
            serviceId: service.id,
            status: 'degraded',
            latency,
            checkedAt,
            error: `Campo ${key} inesperado`
          };
        }
      }
    }

    // Verificar latência para degraded
    const status = latency > DEGRADED_LATENCY_THRESHOLD ? 'degraded' : 'online';

    return {
      serviceId: service.id,
      status,
      latency,
      checkedAt
    };

  } catch (error) {
    const latency = Math.round(performance.now() - startTime);

    return {
      serviceId: service.id,
      status: 'offline',
      latency,
      checkedAt,
      error: error instanceof Error ? error.message : 'Erro desconhecido'
    };
  }
}

export async function checkAllServices(): Promise<StatusPageData> {
  const results = await Promise.all(
    services
      .filter(s => s.healthEndpoint !== null)
      .map(checkService)
  );

  // Propagar status para serviços verificados via outro
  for (const service of services.filter(s => s.checkVia)) {
    const parentResult = results.find(r => r.serviceId === service.checkVia);
    results.push({
      serviceId: service.id,
      status: parentResult?.status || 'unknown',
      latency: null,
      checkedAt: new Date(),
      error: parentResult?.status === 'online' ? undefined : `Depende de ${service.checkVia}`
    });
  }

  // Calcular status geral
  const criticalServices = services.filter(s => s.critical);
  const criticalResults = results.filter(r =>
    criticalServices.some(s => s.id === r.serviceId)
  );

  const criticalOffline = criticalResults.filter(r => r.status === 'offline').length;
  const anyDegraded = results.some(r => r.status === 'degraded');

  let overallStatus: StatusPageData['overallStatus'];
  if (criticalOffline > 0) {
    overallStatus = 'major_outage';
  } else if (anyDegraded) {
    overallStatus = 'degraded';
  } else {
    overallStatus = 'operational';
  }

  return {
    results,
    overallStatus,
    lastUpdated: new Date()
  };
}
```

### API Endpoint

```typescript
// src/pages/api/health.ts
import type { APIRoute } from 'astro';
import { checkAllServices } from '../../lib/health/checker';

export const GET: APIRoute = async () => {
  const data = await checkAllServices();

  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    }
  });
};
```

### Componente StatusGrid

```astro
---
// src/components/StatusGrid.astro
import type { StatusPageData } from '../config/services';
import StatusCard from './StatusCard.astro';

interface Props {
  data: StatusPageData;
}

const { data } = Astro.props;

const statusColors = {
  operational: '#22c55e',
  degraded: '#eab308',
  major_outage: '#ef4444'
};

const statusLabels = {
  operational: 'Todos os sistemas operacionais',
  degraded: 'Performance degradada',
  major_outage: 'Indisponibilidade detectada'
};
---

<div class="status-page">
  <div class="overall-status" style={`border-color: ${statusColors[data.overallStatus]}`}>
    <span class="status-indicator" style={`background: ${statusColors[data.overallStatus]}`}></span>
    <span class="status-label">{statusLabels[data.overallStatus]}</span>
  </div>

  <div class="services-grid">
    {data.results.map(result => (
      <StatusCard result={result} />
    ))}
  </div>

  <p class="last-updated">
    Última verificação: {data.lastUpdated.toLocaleString('pt-BR')}
  </p>
</div>

<style>
  .status-page {
    max-width: 800px;
    margin: 0 auto;
  }

  .overall-status {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border: 2px solid;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }

  .status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }

  .services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }

  .last-updated {
    margin-top: 2rem;
    text-align: center;
    color: var(--sl-color-gray-3);
    font-size: 0.875rem;
  }
</style>
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
