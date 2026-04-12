---
type: rnf
status: review
updated: 2026-02-07
---

# RNF-017: Expiracao de Tokens

## Descricao

Access tokens e refresh tokens devem ter expiracao configurada para equilibrar seguranca e experiencia do usuario. Aplica-se aos modulos Keycloak e GEOAPI.

## Metricas

- TTL access token: 5 minutos (300 segundos)
- SSO session idle: 30 minutos (1800 segundos)
- SSO session max: 10 horas (36000 segundos)
- Offline token idle (REURBCAD mobile): 30 dias
- Configuracao: Keycloak realm settings (realm-export.json)

## Criterios de Aceitacao

1. Access tokens expiram em exatamente 5 minutos
2. SSO session encerra apos 30 minutos de inatividade ou 10 horas absolutas
3. REURBCAD com scope offline_access mantem refresh token por 30 dias para operacao em campo
4. Renovacao automatica de access tokens implementada nos clientes
