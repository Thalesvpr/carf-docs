# Troubleshoot Autenticação

## Usuário não consegue logar

### Verificar se usuário existe
```bash
TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" | jq -r '.access_token')

curl -s "http://localhost:8080/admin/realms/carf/users?username=joao.silva" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Verificar se está habilitado
```bash
# Enabled deve ser true
curl -s "http://localhost:8080/admin/realms/carf/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.enabled'
```

### Resetar senha
```bash
curl -X PUT "http://localhost:8080/admin/realms/carf/users/$USER_ID/reset-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"password","value":"nova_senha","temporary":false}'
```

## Token expirado

### Configuração de timeout
```bash
# Ver configuração atual
curl -s http://localhost:8080/admin/realms/carf \
  -H "Authorization: Bearer $TOKEN" | jq '.accessTokenLifespan'

# Atualizar (em segundos)
curl -X PUT http://localhost:8080/admin/realms/carf \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accessTokenLifespan": 3600}'
```

### Refresh token
```javascript
// Frontend - auto refresh
useEffect(() => {
  const interval = setInterval(() => {
    keycloak.updateToken(30); // refresh se expirar em < 30s
  }, 10000);
  return () => clearInterval(interval);
}, []);
```

## CORS errors

### Configurar Web Origins no client
```bash
curl -X PUT "http://localhost:8080/admin/realms/carf/clients/$CLIENT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "webOrigins": ["http://localhost:3000", "https://app.carf.gov.br"]
  }'
```

## Redirect URI mismatch

### Adicionar redirect URIs válidas
```bash
curl -X PUT "http://localhost:8080/admin/realms/carf/clients/$CLIENT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "redirectUris": [
      "http://localhost:3000/*",
      "https://app.carf.gov.br/*",
      "carf://callback"
    ]
  }'
```

## Client secret inválido

### Verificar secret atual
```bash
curl -s "http://localhost:8080/admin/realms/carf/clients/$CLIENT_ID/client-secret" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.value'
```

### Comparar com .env
```bash
grep KEYCLOAK_CLIENT_SECRET .env
```

## Tenant errado no JWT

### Verificar attributes do usuário
```bash
curl -s "http://localhost:8080/admin/realms/carf/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.attributes'

# Deve ter: "tenants": [...], "current_tenant": ["..."]
```

### Verificar protocol mapper
```bash
curl -s "http://localhost:8080/admin/realms/carf/client-scopes/profile/protocol-mappers/models" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | select(.name == "tenant_id")'
```

## Logs do Keycloak
```bash
# Ver logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f keycloak

# Filtrar erros de autenticação
docker-compose logs keycloak | grep -i "login\|error\|failed"

# Aumentar log level
KC_LOG_LEVEL=debug docker-compose up -d
```
