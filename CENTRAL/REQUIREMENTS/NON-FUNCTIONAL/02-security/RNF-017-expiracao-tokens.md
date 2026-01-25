---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-017: Expiracao de Tokens

## Descricao

Access tokens e refresh tokens devem ter expiracao configurada para equilibrar seguranca e experiencia do usuario. Aplica-se aos modulos Keycloak e GEOAPI.

## Metricas

- TTL access token: 15 minutos
- TTL refresh token: 7 dias
- Configuracao: Keycloak realm/client settings

## Criterios de Aceitacao

1. Access tokens expiram em exatamente 15 minutos
2. Refresh tokens expiram em 7 dias
3. Renovacao automatica de access tokens implementada nos clientes
