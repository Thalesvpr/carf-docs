---
type: leaf
status: review
updated: 2026-02-07
---

# Realm Export Schema

Estrutura JSON do realm-export.json para versionamento de configuracao como codigo. Importavel via --import-realm no startup.

## Estrutura Raiz

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| id | string | Sim | Identificador interno |
| realm | string | Sim | Nome do realm em URLs |
| displayName | string | Nao | Nome amigavel |
| enabled | boolean | Nao | Realm ativo (default true) |

## SSL e Seguranca

| Campo | Tipo | Default | Descricao |
|:------|:-----|:--------|:----------|
| sslRequired | string | external | all, external, none |
| bruteForceProtected | boolean | false | Protecao brute force |
| permanentLockout | boolean | false | Lock permanente |
| maxFailureWaitSeconds | int | 900 | Wait maximo (15 min) |
| failureFactor | int | 5 | Tentativas antes de lock |

## Registro e Login

| Campo | Tipo | Default | Descricao |
|:------|:-----|:--------|:----------|
| registrationAllowed | boolean | false | Auto-registro |
| loginWithEmailAllowed | boolean | true | Login com email |
| duplicateEmailsAllowed | boolean | false | Emails duplicados |
| resetPasswordAllowed | boolean | false | Recuperacao de senha |
| verifyEmail | boolean | false | Verificacao de email |
| rememberMe | boolean | false | Opcao lembrar-me |

## Token Lifespans

| Campo | Tipo | Default | Descricao |
|:------|:-----|:--------|:----------|
| accessTokenLifespan | int | 300 | Access token (5 min) |
| ssoSessionIdleTimeout | int | 1800 | Idle SSO (30 min) |
| ssoSessionMaxLifespan | int | 36000 | Max SSO (10h) |
| offlineSessionIdleTimeout | int | 2592000 | Idle offline (30 dias) |
| accessCodeLifespan | int | 60 | Auth code (1 min) |

## Temas e Internacionalizacao

Campos de tema: loginTheme, accountTheme, adminTheme e emailTheme. No CARF, login, account e email usam carf, admin usa keycloak.v2. Internacionalizacao com supportedLocales pt-BR e en, defaultLocale pt-BR.

Ver [06a-realm-export-clients](./06a-realm-export-clients.md) para clients e [06b-realm-export-roles](./06b-realm-export-roles.md) para roles.
