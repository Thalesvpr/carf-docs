# Integração API

Guia completo de integração com a API REST do CARF GEOAPI.

## Visão Geral

A API REST do CARF permite integração com sistemas externos para gerenciamento de dados de regularização fundiária urbana (REURB).

## Autenticação

### OAuth2 com Keycloak

A API utiliza OAuth2 via Keycloak para autenticação e autorização.

```bash
# Obter token de acesso
curl -X POST "https://keycloak.example.com/realms/carf/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=your-client-id" \
  -d "client_secret=your-client-secret" \
  -d "grant_type=client_credentials"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

### Usando o Token

Todas as requisições devem incluir o token no header:

```bash
curl -X GET "https://api.carf.example.com/api/units" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Endpoints Principais

### Units (Unidades Habitacionais)

#### Listar Unidades

```bash
GET /api/units
```

**Resposta:**
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "code": "UN-001",
      "address": "Rua das Flores, 123",
      "area": 250.5,
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    }
  ],
  "total": 150,
  "page": 1,
  "pageSize": 20
}
```

#### Criar Unidade

```bash
POST /api/units
Content-Type: application/json

{
  "code": "UN-002",
  "address": "Rua das Palmeiras, 456",
  "area": 180.0,
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-46.6333, -23.5505], ...]]
  }
}
```

### Holders (Possuidores)

#### Listar Possuidores

```bash
GET /api/holders
```

#### Vincular Possuidor a Unidade

```bash
POST /api/holders/{holderId}/units/{unitId}
```

### Communities (Comunidades)

#### Listar Comunidades

```bash
GET /api/communities
```

#### Obter Unidades de uma Comunidade

```bash
GET /api/communities/{communityId}/units
```

## Paginação

A API suporta paginação via query parameters:

```bash
GET /api/units?page=2&pageSize=50
```

## Filtros

### Filtro por Geometria

Buscar unidades dentro de um polígono:

```bash
POST /api/units/search/within
Content-Type: application/json

{
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-46.6333, -23.5505], ...]]
  }
}
```

### Filtro por Raio

Buscar unidades em um raio de 500m:

```bash
GET /api/units/search/radius?lat=-23.5505&lng=-46.6333&radius=500
```

## Tratamento de Erros

### Códigos de Status HTTP

- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Token ausente ou inválido
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro no servidor

### Formato de Erro

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      {
        "field": "area",
        "message": "Área deve ser maior que zero"
      }
    ]
  }
}
```

## Rate Limiting

A API possui limite de requisições:

- **100 requisições/minuto** por cliente
- Headers de resposta:
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 85`
  - `X-RateLimit-Reset: 1640995200`

## Webhooks

Configure webhooks para receber notificações de eventos:

```bash
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["unit.created", "unit.updated", "holder.created"],
  "secret": "your-webhook-secret"
}
```

## SDKs e Bibliotecas

### JavaScript/TypeScript

```bash
npm install @carf/api-client
```

```typescript
import { CarfApiClient } from '@carf/api-client';

const client = new CarfApiClient({
  baseUrl: 'https://api.carf.example.com',
  token: 'your-access-token'
});

const units = await client.units.list({ page: 1, pageSize: 20 });
```

### C#

```bash
dotnet add package Carf.ApiClient
```

```csharp
using Carf.ApiClient;

var client = new CarfApiClient("https://api.carf.example.com", "your-access-token");
var units = await client.Units.ListAsync(page: 1, pageSize: 20);
```

## Recursos Adicionais

- [API Reference completa](/dev/api/)
- [Documentação Swagger](https://api.carf.example.com/swagger)
- [Exemplos no GitHub](https://github.com/Thalesvpr/carf-api-examples)

## Suporte

Para dúvidas ou problemas:
- Abra uma issue no [GitHub](https://github.com/Thalesvpr/carf-geoapi/issues)
- Entre em contato: suporte@carf.example.com
