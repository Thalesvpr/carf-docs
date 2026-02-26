# Pós-Deploy HML — Checklist Keycloak

Depois do `docker compose up -d --build`, o Keycloak importa o realm `carf` automaticamente.
Os clients estão configurados para `localhost`. Atualize os redirect URIs para HML.

## 1. Acessar Keycloak Admin

- URL: `http://hml-auth.IP.sslip.io/admin`
- Login: valores de `KC_ADMIN_USER` / `KC_ADMIN_PASSWORD` do `.env`

## 2. Atualizar client `reurbweb`

Realm: `carf` → Clients → `reurbweb`

| Campo | Valor |
|---|---|
| Root URL | `http://hml-app.IP.sslip.io` |
| Valid Redirect URIs | `http://hml-app.IP.sslip.io/*` |
| Valid Post Logout Redirect URIs | `http://hml-app.IP.sslip.io/*` |
| Web Origins | `http://hml-app.IP.sslip.io` |

## 3. Atualizar client `reurbmaster`

Realm: `carf` → Clients → `reurbmaster`

| Campo | Valor |
|---|---|
| Root URL | `http://hml-admin.IP.sslip.io` |
| Valid Redirect URIs | `http://hml-admin.IP.sslip.io/*` |
| Valid Post Logout Redirect URIs | `http://hml-admin.IP.sslip.io/*` |
| Web Origins | `http://hml-admin.IP.sslip.io` |

## 4. Atualizar (ou criar) client `geoapi-admin`

Realm: `carf` → Clients → `geoapi-admin`

Se não existir, crie:

| Campo | Valor |
|---|---|
| Client ID | `geoapi-admin` |
| Client Authentication | ON (confidential) |
| Service accounts roles | ON |
| Valid Redirect URIs | `http://hml-api.IP.sslip.io/*` |

Depois de criar:
1. Aba **Credentials** → copiar **Client Secret**
2. Colar no `.env` em `KC_GEOAPI_CLIENT_SECRET`
3. `docker compose restart geoapi`

## 5. Criar usuário de teste

Realm: `carf` → Users → Add user

| Campo | Valor |
|---|---|
| Username | `dev@carf.com` |
| Email | `dev@carf.com` |
| Email verified | ON |
| First name | Dev |
| Last name | HML |

Depois:
1. Aba **Credentials** → Set password: `Dev@1234` (temporary OFF)
2. Aba **Attributes** → adicionar:
   - `current_tenant` = ID do tenant (criar via API depois)
   - `tenants` = mesmo ID
3. Aba **Role Mappings** → atribuir roles

## 6. Testar fluxo completo

1. `http://hml-app.IP.sslip.io` → redireciona pro Keycloak → login → REURBWEB
2. `http://hml-api.IP.sslip.io/swagger` → Swagger
3. `http://hml-admin.IP.sslip.io` → REURBMASTER
4. `http://hml-s3.IP.sslip.io` → MinIO Console
5. `http://hml-auth.IP.sslip.io/admin` → Keycloak Admin
