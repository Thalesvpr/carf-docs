---
type: standard
status: approved
updated: 2026-01-22
---

# STD-012: Keycloak para Autenticacao

## Regra

Toda autenticacao e autorizacao deve usar Keycloak como Identity Provider. Proibido implementar auth customizado, usar Auth0, Firebase Auth ou Cognito.

## Justificativa

OAuth2/OIDC completo, multi-realm para isolamento de tenants, RBAC granular, MFA nativo, SSO entre aplicacoes, auditoria integrada. Open-source sem custo de licensing.

## Aplicacao

Todos os projetos CARF. Single Sign-On entre GEOAPI, GEOWEB, REURBCAD, GEOGIS, ADMIN. Cada prefeitura em realm separado.
