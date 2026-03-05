# Pos-Deploy HML

## O que e automatico

O `keycloak-init` container cuida de tudo automaticamente ao rodar `docker compose up -d --build`:

- Desabilita SSL required nos realms `master` e `carf`
- Atualiza redirect URIs do `reurbweb` e `reurbmaster` para o IP do HML
- Preserva localhost nos redirect URIs (dev local continua funcionando)
- Cria usuario `admin.hml` com senha (ver `KC_SEED_USER_PASSWORD` no `.env`)
- Atribui roles `super-admin`, `admin`, `dev`
- Define atributos de tenant (`current_tenant=default`, `tenants=default`)
- Monta o tema CARF no Keycloak (tela de login customizada)

## Verificar se o init rodou

```bash
docker logs carf-hml-keycloak-init
```

Todos os passos devem mostrar `[ok]`. O container termina com exit 0.

## Unica verificacao manual: geoapi-admin secret

O client `geoapi-admin` vem com secret `changeme` do realm-export.json.
Se voce trocou `KC_GEOAPI_CLIENT_SECRET` no `.env`, confirme que bate com o Keycloak:

```bash
docker exec carf-hml-keycloak \
  /opt/keycloak/bin/kcadm.sh config credentials \
    --server http://localhost:8080 --realm master \
    --user admin --password 'SUA_SENHA'

docker exec carf-hml-keycloak \
  /opt/keycloak/bin/kcadm.sh get clients -r carf -q clientId=geoapi-admin \
    --fields id,clientId,serviceAccountsEnabled

# Ver o secret atual (substituir CLIENT_ID)
docker exec carf-hml-keycloak \
  /opt/keycloak/bin/kcadm.sh get clients/CLIENT_ID/client-secret -r carf
```

## Testar fluxo completo

| # | Teste | URL | Esperado |
|---|-------|-----|----------|
| 1 | REURBWEB | `http://hml-app.IP.sslip.io` | Login com tema CARF (nao tema padrao Keycloak) |
| 2 | Login | (tela do Keycloak) | Login com admin.hml / Dev@1234 |
| 3 | Dashboard | (apos login) | Dashboard do REURBWEB |
| 4 | REURBMASTER | `http://hml-admin.IP.sslip.io` | Login + dashboard admin |
| 5 | Swagger | `http://hml-api.IP.sslip.io/swagger` | Swagger UI |
| 6 | Keycloak admin | `http://hml-auth.IP.sslip.io/admin` | Admin console (sem erro "HTTPS required") |
| 7 | MinIO | `http://hml-s3.IP.sslip.io` | MinIO console |

## Troubleshooting

### keycloak-init falha ao autenticar

As env vars `KEYCLOAK_ADMIN`/`KEYCLOAK_ADMIN_PASSWORD` so criam o admin no **primeiro boot**.
Se o volume persistiu de um deploy anterior com senha diferente:

```bash
# Resetar o admin (o erro "Address already in use" no final e esperado)
docker exec \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD='NOVA_SENHA' \
  carf-hml-keycloak \
  /opt/keycloak/bin/kc.sh bootstrap-admin user \
    --username admin \
    --password:env KC_BOOTSTRAP_ADMIN_PASSWORD \
    --no-prompt

docker compose restart keycloak
# Atualizar KC_ADMIN_PASSWORD no .env, depois:
docker compose up -d keycloak-init
```

### GEOAPI retorna 500

Causa mais comum: `RequireHttpsMetadata=true` quando Keycloak roda HTTP.

```bash
docker compose logs geoapi --tail 20
```

O docker-compose.yml ja define `ASPNETCORE_ENVIRONMENT: Development` que desabilita o check.

### Frontends retornam 403 no build

O token NPM nao tem acesso ao GitHub Packages da org `carffundiaria`.

```bash
curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $NPM_TOKEN" \
  https://npm.pkg.github.com/@carffundiaria/ui
# 200 ou 302 = OK. 401/403 = sem acesso.
```

### Re-executar o init manualmente

```bash
docker compose up -d keycloak-init
docker logs -f carf-hml-keycloak-init
```
