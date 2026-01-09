# Criar Usuário no Keycloak

## Via Admin Console
1. Acesse http://localhost:8080 → Admin Console
2. Realm: `carf`
3. Users → Create new user
4. Username: `cpf-do-usuario` ou `email@example.com`
5. Email: preencher
6. Attributes → Add:
   - `tenants`: `["tenant1", "tenant2"]`
   - `current_tenant`: `tenant1`
7. Credentials → Set password (desmarcar "Temporary")
8. Role mapping → Assign role: `user`, `admin`, etc.

## Via Admin API
```bash
# Get admin token
TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" | jq -r '.access_token')

# Create user
curl -X POST http://localhost:8080/admin/realms/carf/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao.silva",
    "email": "joao@example.com",
    "enabled": true,
    "emailVerified": false,
    "attributes": {
      "tenants": ["tenant1"],
      "current_tenant": ["tenant1"]
    },
    "credentials": [{
      "type": "password",
      "value": "senha123",
      "temporary": false
    }]
  }'

# Assign role
USER_ID=$(curl -s http://localhost:8080/admin/realms/carf/users?username=joao.silva \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[0].id')

ROLE_ID=$(curl -s http://localhost:8080/admin/realms/carf/roles/user \
  -H "Authorization: Bearer $TOKEN" | jq -r '.id')

curl -X POST "http://localhost:8080/admin/realms/carf/users/$USER_ID/role-mappings/realm" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "[{\"id\":\"$ROLE_ID\",\"name\":\"user\"}]"
```

## Verificação
```bash
# Login do usuário
curl -X POST http://localhost:8080/realms/carf/protocol/openid-connect/token \
  -d "client_id=geoweb" \
  -d "grant_type=password" \
  -d "username=joao.silva" \
  -d "password=senha123" | jq '.access_token' | cut -d. -f2 | base64 -d | jq
```
