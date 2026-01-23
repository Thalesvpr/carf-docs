---
type: leaf
status: review
updated: 2026-01-22
---

# KEYCLOAK

Identity provider centralizado que gerencia autenticacao e autorizacao para todos os sistemas do ecossistema CARF. Implementa OAuth2 e OpenID Connect fornecendo single sign-on entre aplicacoes web, mobile e desktop.

Configurado com single realm CARF contendo todos os usuarios e clients. Multi-tenancy implementado via atributo tenant_id no usuario com claims customizados no token. Hierarquia de 5 roles define permissoes desde agente de campo ate administrador de plataforma. Temas customizados com Keycloakify reutilizando componentes @carf/ui.

## Capacidades

Fluxos OAuth2 diferenciados por tipo de client: Authorization Code com PKCE para web e mobile, Client Credentials para backend-to-backend. Validacao de CPF customizada no registro. Politicas de senha e MFA configuradas por tenant. Session management com token lifetimes otimizados por contexto de uso. Detalhes tecnicos em [PROJECTS/KEYCLOAK/DOCS/](../../../PROJECTS/KEYCLOAK/DOCS/README.md).
