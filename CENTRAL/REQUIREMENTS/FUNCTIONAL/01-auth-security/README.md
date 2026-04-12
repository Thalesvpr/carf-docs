---
type: readme
status: approved
updated: 2026-01-25
---

# Autenticacao e Seguranca

Requisitos funcionais de autenticacao, autorizacao e seguranca do ecossistema CARF. Define integracao com Keycloak como identity provider centralizado, fluxos OAuth2 para diferentes tipos de aplicacao e modelo de controle de acesso baseado em roles.

Os requisitos [RF-001](./RF-001-integração-com-keycloak.md) a [RF-005](./RF-005-validação-jwt-em-todas-requisições.md) cobrem integracao OAuth2 com Keycloak incluindo fluxos Authorization Code PKCE para web, autenticacao do plugin QGIS com AUTHENTICATION KEY e validacao JWT. Os requisitos [RF-006](./RF-006-6-níveis-de-acesso-roles.md) a [RF-011](./RF-011-equipe-campo-coleta-de-dados.md) definem os 6 niveis hierarquicos de acesso (SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR). Os requisitos [RF-012](./RF-012-controle-de-acesso-por-recurso.md) a [RF-016](./RF-016-auditoria-de-acessos.md) tratam de controle granular por recurso, isolamento multi-tenant e auditoria.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (16)

| Documento | Status |
|-----------|--------|
| [RF-001: Integracao com Keycloak](./RF-001-integração-com-keycloak.md) | ⚠ |
| [RF-002: Fluxo Authorization Code PKCE](./RF-002-fluxo-authorization-code-pkce.md) | ⚠ |
| [RF-003: Autenticacao Plugin QGIS](./RF-003-client-credentials-flow.md) | ⚠ |
| [RF-004: Refresh Token Automatico](./RF-004-refresh-token-automático.md) | ⚠ |
| [RF-005: Validacao JWT em Todas Requisicoes](./RF-005-validação-jwt-em-todas-requisições.md) | ⚠ |
| [RF-006: 6 Niveis de Acesso (Roles)](./RF-006-6-níveis-de-acesso-roles.md) | ⚠ |
| [RF-007: SUPER_ADMIN - Acesso Total](./RF-007-super_admin-acesso-total.md) | ⚠ |
| [RF-008: ADMIN - Gestao de Tenant](./RF-008-admin-gestão-de-tenant.md) | ⚠ |
| [RF-009: MANAGER - Aprovacao de Workflows](./RF-009-manager-aprovação-de-workflows.md) | ⚠ |
| [RF-010: ANALYST - Cadastro e Edicao](./RF-010-analyst-cadastro-e-edição.md) | ⚠ |
| [RF-011: Equipe de Campo - Coleta de Dados](./RF-011-equipe-campo-coleta-de-dados.md) | ⚠ |
| [RF-012: Controle de Acesso por Recurso](./RF-012-controle-de-acesso-por-recurso.md) | ⚠ |
| [RF-013: Isolamento de Dados por Tenant](./RF-013-isolamento-de-dados-por-tenant.md) | ⚠ |
| [RF-014: Logout e Revogacao de Token](./RF-014-logout-e-revogação-de-token.md) | ⚠ |
| [RF-015: Sessao Expirada - Redirecionamento](./RF-015-sessão-expirada-redirecionamento.md) | ⚠ |
| [RF-016: Auditoria de Acessos](./RF-016-auditoria-de-acessos.md) | ⚠ |

<!-- CARF-INDEX-END -->
