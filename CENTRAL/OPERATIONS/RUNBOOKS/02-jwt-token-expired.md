# JWT Token Expired

Runbook para resolver problemas de tokens JWT expirados ou inválidos retornados pelo Keycloak, indicados por erros 401 Unauthorized com mensagem "token expired" ou "invalid token".

## Diagnóstico

```bash
# Decodificar token JWT (sem validar assinatura)
echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq .

# Verificar claims importantes
echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq '{exp: .exp, iat: .iat, sub: .sub, tenant_id: .tenant_id}'

# Converter timestamp exp para data
date -d @$(echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq -r .exp)
```

## Verificar Keycloak

```bash
# Status do Keycloak
kubectl get pods -l app=keycloak

# Logs de autenticação
kubectl logs -l app=keycloak --tail=200 | grep -i "token\|expired\|invalid"

# Verificar realm config via API
curl -s -X GET "https://keycloak.carf.com.br/admin/realms/carf" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.accessTokenLifespan, .ssoSessionIdleTimeout'
```

## Ações Imediatas

```bash
# Forçar refresh token no cliente (frontend)
# O cliente deve chamar /token com grant_type=refresh_token

# Invalidar todas as sessões de um usuário (se comprometido)
curl -X POST "https://keycloak.carf.com.br/admin/realms/carf/users/{user-id}/logout" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Verificar clock skew entre servidores
kubectl exec -it deploy/geoapi -- date
kubectl exec -it deploy/keycloak -- date
```

## Configuração de Tokens

Keycloak Realm Settings recomendados:
- Access Token Lifespan: 5 minutos (300 segundos)
- Refresh Token Lifespan: 30 minutos
- SSO Session Idle: 30 minutos
- SSO Session Max: 8 horas

GEOAPI validação (`appsettings.json`):
```json
{
  "Authentication": {
    "Keycloak": {
      "Authority": "https://keycloak.carf.com.br/realms/carf",
      "ValidateLifetime": true,
      "ClockSkew": "00:00:30"
    }
  }
}
```

## Problemas Comuns

1. **Clock skew**: Diferença de horário entre servidores causa rejeição prematura. Sincronizar NTP.
2. **Refresh falhou**: Token de refresh também expirou. Usuário precisa re-autenticar.
3. **Revogação**: Token foi revogado administrativamente. Verificar audit logs do Keycloak.

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
