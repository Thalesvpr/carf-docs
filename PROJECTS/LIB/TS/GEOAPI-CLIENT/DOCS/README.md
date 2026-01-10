# GEOAPI-CLIENT - Documentação Específica de Implementação

Cliente HTTP TypeScript para comunicação com a API GEOAPI do projeto CARF.

## Visão Geral

O **@carf/geoapi-client** é um SDK TypeScript que fornece uma interface tipada e robusta para consumir os endpoints da API REST GEOAPI. Ele encapsula toda a lógica de comunicação HTTP, tratamento de erros, autenticação e retry.

## Estrutura da Documentação

### ARCHITECTURE/
Decisões arquiteturais e design do cliente HTTP.

- **01-client-architecture.md** - Arquitetura geral do cliente
- **02-error-handling.md** - Estratégia de tratamento de erros
- **03-authentication-flow.md** - Fluxo de autenticação com tokens
- **04-retry-strategy.md** - Estratégia de retry e circuit breaker

### CONCEPTS/
Conceitos fundamentais sobre o SDK.

- **01-http-client.md** - Cliente HTTP base (Axios/Fetch)
- **02-interceptors.md** - Interceptors de request/response
- **03-type-safety.md** - Type safety e validação em runtime
- **04-offline-support.md** - Suporte offline (caching)

### HOW-TO/
Guias práticos de uso e integração.

- **01-installation.md** - Como instalar e configurar
- **02-basic-usage.md** - Uso básico do cliente
- **03-authentication.md** - Como configurar autenticação
- **04-error-handling.md** - Como tratar erros
- **05-testing.md** - Como testar aplicações que usam o SDK
- **06-advanced-usage.md** - Uso avançado (custom interceptors, etc)

### API/
Referência completa da API do SDK.

- **01-geoapi-client.md** - Classe principal `GeoApiClient`
- **02-units-api.md** - `UnitsApi` - CRUD de unidades
- **03-holders-api.md** - `HoldersApi` - Gerenciamento de posseiros
- **04-communities-api.md** - `CommunitiesApi` - Comunidades
- **05-legitimation-api.md** - `LegitimationApi` - Processos de legitimação
- **06-reports-api.md** - `ReportsApi` - Geração de relatórios
- **07-authentication-api.md** - `AuthenticationApi` - Login/logout

## Relação com CENTRAL/

Este SDK implementa o cliente para os endpoints documentados em:
- [CENTRAL/API/](../../../../../CENTRAL/API/README.md) - Especificação dos endpoints REST
- [CENTRAL/INTEGRATION/KEYCLOAK/](../../../../../CENTRAL/INTEGRATION/KEYCLOAK/README.md) - Autenticação OAuth2

## Relação com outros projetos

### Dependências
- **@carf/tscore** - Types, validações, KeycloakClient

### Consumidores
- **GEOWEB** - Frontend React web
- **REURBCAD** - App React Native mobile
- **ADMIN** - Console administrativo React
- **WEBDOCS** - Exemplos de código na documentação

## Tecnologias

- **TypeScript** 5.3+
- **Axios** 1.6+ (HTTP client)
- **Zod** 3.22+ (runtime validation)
- **@carf/tscore** (auth + types)
- **Bun** (runtime e bundler)

## Features

✅ **Type-safe** - Totalmente tipado com TypeScript
✅ **Auto-authentication** - Injeta tokens automaticamente
✅ **Error handling** - Erros tipados e tratados
✅ **Retry logic** - Retry automático em falhas transientes
✅ **Request/Response interceptors** - Customizáveis
✅ **Offline support** - Cache de requisições (opcional)
✅ **Pagination** - Helpers para paginação
✅ **File upload** - Suporte a upload de arquivos
✅ **Streaming** - Download de arquivos grandes

## Quick Start

```typescript
import { GeoApiClient } from '@carf/geoapi-client';
import { KeycloakClient } from '@carf/tscore/auth';

// Setup auth
const auth = new KeycloakClient({
  url: 'https://keycloak.carf.gov.br',
  realm: 'carf',
  clientId: 'geoweb-client'
});

// Create API client
const api = new GeoApiClient({
  baseURL: 'https://api.carf.gov.br',
  auth: auth,
  timeout: 30000
});

// Use API
const units = await api.units.list({ page: 1, limit: 10 });
const unit = await api.units.getById('123');
const newUnit = await api.units.create({
  address: 'Rua Example, 123',
  coordinates: { lat: -23.5505, lng: -46.6333 }
});
```

## Instalação

```bash
# Com Bun
bun add @carf/geoapi-client @carf/tscore

# Com npm
npm install @carf/geoapi-client @carf/tscore

# Com yarn
yarn add @carf/geoapi-client @carf/tscore
```

## Links Úteis

- **GEOAPI Backend Documentation**
- [CENTRAL API Specification](../../../../../CENTRAL/API/README.md)
- [TSCORE Documentation](../../TSCORE/DOCS/README.md)
- [Axios Documentation](https://axios-http.com/docs/intro)
