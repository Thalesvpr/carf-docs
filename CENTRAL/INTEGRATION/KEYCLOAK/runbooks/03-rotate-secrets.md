# Rotacionar Secrets

## Client Secrets (sem downtime)

### 1. Gerar novo secret
```bash
TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" | jq -r '.access_token')

# Regenerate secret
NEW_SECRET=$(curl -X POST "http://localhost:8080/admin/realms/carf/clients/geoapi-client-id/client-secret" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.value')

echo "Novo secret: $NEW_SECRET"
```

### 2. Atualizar aplicações
```bash
# Atualizar .env das aplicações
echo "KEYCLOAK_CLIENT_SECRET=$NEW_SECRET" >> GEOAPI/.env

# Restart aplicação
docker-compose restart geoapi
```

## Admin Password

### 1. Via Admin Console
1. Acesse Admin Console
2. Users → admin → Credentials
3. Reset password

### 2. Via CLI (container parado)
```bash
docker-compose -f docker-compose.dev.yml down

docker-compose -f docker-compose.dev.yml run --rm \
  -e KEYCLOAK_ADMIN_PASSWORD=nova_senha_forte \
  keycloak start-dev --import-realm

docker-compose -f docker-compose.dev.yml up -d
```

## PostgreSQL Password

### Zero downtime
```sql
-- 1. Criar novo user
CREATE USER keycloak_new WITH PASSWORD 'nova_senha_forte';
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_new;

-- 2. Atualizar .env
KC_DB_USERNAME=keycloak_new
KC_DB_PASSWORD=nova_senha_forte

-- 3. Restart Keycloak
docker-compose restart keycloak

-- 4. Remover old user
DROP USER keycloak;
```

## Quando Rotacionar
- Client secrets: a cada 90 dias
- Admin password: a cada 90 dias
- PostgreSQL password: a cada 180 dias
- Após suspeita de vazamento: imediatamente

## Automação
```bash
# Cron job mensal
0 0 1 * * /path/to/carf-keycloak/scripts/rotate-secrets.sh
```
