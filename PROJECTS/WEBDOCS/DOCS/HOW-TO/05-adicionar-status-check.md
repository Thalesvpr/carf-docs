---
status: review
updated: 2026-01-21
---

# Adicionar Status Check

Guia para incluir novo serviço na status page permitindo monitorar disponibilidade.

Identificar endpoint de health do serviço a monitorar. Endpoint deve retornar HTTP 200 quando serviço está saudável e código de erro quando não está. Response pode incluir detalhes em JSON mas não é obrigatório.

Editar arquivo de configuração em src/config/services.ts que define array de serviços monitorados. Cada serviço tem id único usado internamente, name para exibição na interface, url do endpoint de health, e timeout em milissegundos.

Adicionar entrada para novo serviço com id descritivo em kebab-case, name legível para usuários, url completa do endpoint de health, e timeout apropriado (5000ms padrão, aumentar para serviços lentos).

Testar localmente executando bun run dev e acessando /status/. Novo serviço deve aparecer na lista com indicador de status. Verificar que status reflete corretamente disponibilidade do serviço.

Configurar variável de ambiente se URL do serviço diferir entre ambientes. Usar process.env para ler variável em services.ts. Adicionar variável em .env.example com valor de exemplo e documentar.

Considerar autenticação se endpoint de health requer token. Status page executa fetch server-side então token pode ser incluído em header sem expor ao cliente. Armazenar token em variável de ambiente.

Commit e push da mudança. Pipeline de CI valida build. Preview deployment permite testar em ambiente similar a produção antes de merge.

## Estrutura do Arquivo de Configuração

```typescript
// src/config/services.ts
export interface Service {
  id: string;
  name: string;
  description: string;
  healthEndpoint: string | null;
  timeout: number;
  critical: boolean;
  category: 'api' | 'database' | 'auth' | 'external';
  expectedResponse?: {
    status: number;
    bodyContains?: string;
  };
}

export const services: Service[] = [
  {
    id: 'geoapi',
    name: 'GeoAPI',
    description: 'API principal de dados geoespaciais',
    healthEndpoint: import.meta.env.GEOAPI_URL + '/health',
    timeout: 5000,
    critical: true,
    category: 'api',
    expectedResponse: {
      status: 200,
      bodyContains: '"status":"healthy"'
    }
  },
  {
    id: 'keycloak',
    name: 'Keycloak',
    description: 'Servidor de autenticação',
    healthEndpoint: import.meta.env.KEYCLOAK_URL + '/health/ready',
    timeout: 5000,
    critical: true,
    category: 'auth',
    expectedResponse: {
      status: 200
    }
  },
  {
    id: 'postgres',
    name: 'PostgreSQL',
    description: 'Banco de dados principal',
    healthEndpoint: null, // Checado via GeoAPI
    timeout: 5000,
    critical: true,
    category: 'database'
  }
];
```

## Exemplo: Adicionar Novo Serviço

Para adicionar um serviço de cache Redis:

```typescript
// Adicionar ao array services em src/config/services.ts
{
  id: 'redis',
  name: 'Redis Cache',
  description: 'Cache de sessões e dados temporários',
  healthEndpoint: import.meta.env.REDIS_HEALTH_URL || 'http://localhost:6379/ping',
  timeout: 3000,
  critical: false, // Sistema funciona sem cache
  category: 'database',
  expectedResponse: {
    status: 200,
    bodyContains: 'PONG'
  }
}
```

## Variáveis de Ambiente

```bash
# Adicionar em .env e .env.example
REDIS_HEALTH_URL=http://redis:6379/ping
```

## Serviço com Autenticação

```typescript
// Para serviços que requerem token
{
  id: 'external-api',
  name: 'API Externa',
  description: 'Integração com serviço de terceiros',
  healthEndpoint: 'https://api.externa.com/health',
  timeout: 10000,
  critical: false,
  category: 'external',
  headers: {
    'Authorization': `Bearer ${import.meta.env.EXTERNAL_API_TOKEN}`
  }
}
```

## Checklist

```json
{
  "checklist": [
    "[ ] Identificar endpoint de health do serviço",
    "[ ] Testar endpoint manualmente (curl ou browser)",
    "[ ] Adicionar entrada em src/config/services.ts",
    "[ ] Definir timeout apropriado (padrão 5000ms)",
    "[ ] Marcar critical: true se sistema depende do serviço",
    "[ ] Adicionar variável de ambiente se URL varia por ambiente",
    "[ ] Testar localmente em /status/",
    "[ ] Verificar preview deployment"
  ]
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
