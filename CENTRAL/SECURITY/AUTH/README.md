---
type: readme
status: draft
updated: 2026-01-22
---

# AUTH

Documentacao de autenticacao e autorizacao do sistema CARF baseada em Keycloak.

Esta pasta contem as decisoes arquiteturais sobre o modelo RBAC (Role-Based Access Control) implementado no Keycloak. O documento [01-rbac-keycloak](./01-rbac-keycloak.md) define a estrutura de composite roles com heranca automatica, enquanto [02-roles-hierarchy](./02-roles-hierarchy.md) detalha os cinco niveis operacionais (user, field-agent, analyst, admin, super-admin) e a role transversal dev.

A implementacao pratica destas definicoes esta em [PROJECTS/KEYCLOAK](../../../PROJECTS/KEYCLOAK/README.md). As politicas relacionadas de autenticacao, autorizacao e controle de acesso estao em [POLICIES](../POLICIES/README.md).
