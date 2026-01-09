# API Reference

Documentação dos endpoints REST da GEOAPI (Backend .NET 9).

## Base URL

```
http://localhost:5000/api
```

## Autenticação

Todos os endpoints requerem autenticação OAuth2 via Keycloak:

```http
Authorization: Bearer <access_token>
```

## Domínios

A API está organizada por domínios:

### Units (Unidades Habitacionais)

```http
GET    /api/units
POST   /api/units
GET    /api/units/{id}
PUT    /api/units/{id}
DELETE /api/units/{id}
GET    /api/units/search
```

### Holders (Possuidores/Beneficiários)

```http
GET    /api/holders
POST   /api/holders
GET    /api/holders/{id}
PUT    /api/holders/{id}
DELETE /api/holders/{id}
```

### Communities (Comunidades/Núcleos)

```http
GET    /api/communities
POST   /api/communities
GET    /api/communities/{id}
PUT    /api/communities/{id}
DELETE /api/communities/{id}
```

### Processes (Processos REURB)

```http
GET    /api/processes
POST   /api/processes
GET    /api/processes/{id}
PUT    /api/processes/{id}
DELETE /api/processes/{id}
```

## Contratos Completos

A documentação completa dos contratos REST está disponível em:

- [CENTRAL/API](https://github.com/Thalesvpr/carf-docs/tree/main/CENTRAL/API)

## Swagger/OpenAPI

Em desenvolvimento, acesse:

```
http://localhost:5000/swagger
```

## Multi-Tenancy

Todos os endpoints respeitam automaticamente o isolamento por `tenant_id` via Row-Level Security (RLS) do PostgreSQL.

## Exemplos

### Criar Unidade Habitacional

```http
POST /api/units
Content-Type: application/json
Authorization: Bearer <token>

{
  "address": "Rua Exemplo, 123",
  "coordinates": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "area": 50.5,
  "holderId": "uuid-holder"
}
```

### Resposta

```json
{
  "id": "uuid-unit",
  "address": "Rua Exemplo, 123",
  "coordinates": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "area": 50.5,
  "holderId": "uuid-holder",
  "createdAt": "2026-01-08T21:00:00Z"
}
```
