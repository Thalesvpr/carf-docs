# Criar e Gerenciar Tenants

## Conceito
Tenants no CARF são identificadores em user attributes que aparecem no JWT como `tenant_id`.

## Adicionar Tenant a Usuário
```bash
# Get admin token
TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" | jq -r '.access_token')

# Get user ID
USER_ID=$(curl -s "http://localhost:8080/admin/realms/carf/users?username=joao.silva" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[0].id')

# Update attributes
curl -X PUT "http://localhost:8080/admin/realms/carf/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "attributes": {
      "tenants": ["tenant1", "tenant2", "tenant3"],
      "current_tenant": ["tenant1"]
    }
  }'
```

## Trocar Tenant Ativo
```bash
# Update apenas current_tenant
curl -X PUT "http://localhost:8080/admin/realms/carf/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "attributes": {
      "tenants": ["tenant1", "tenant2", "tenant3"],
      "current_tenant": ["tenant2"]
    }
  }'
```

## Verificar Tenant no JWT
```bash
# Login e decode token
ACCESS_TOKEN=$(curl -X POST http://localhost:8080/realms/carf/protocol/openid-connect/token \
  -d "client_id=geoweb" \
  -d "grant_type=password" \
  -d "username=joao.silva" \
  -d "password=senha123" | jq -r '.access_token')

echo $ACCESS_TOKEN | cut -d. -f2 | base64 -d | jq '.tenant_id'
# Output: "tenant2"
```

## Client-Side Tenant Switcher
```typescript
// React - trocar tenant via Admin API
const switchTenant = async (newTenantId: string) => {
  await adminClient.users.update({
    id: user.sub,
    attributes: {
      tenants: user.tenants,
      current_tenant: [newTenantId]
    }
  });

  // Refresh token para pegar novo tenant_id
  await keycloak.updateToken(5);
};
```

## Isolamento de Dados (Backend)
```csharp
// .NET - RLS com tenant_id do JWT
var tenantId = User.FindFirst("tenant_id")?.Value;
var data = await context.Properties
    .Where(p => p.TenantId == tenantId)
    .ToListAsync();
```
