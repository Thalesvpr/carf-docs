---
type: leaf
status: review
updated: 2026-02-07
---

# KEYCLOAK

Identity provider centralizado que gerencia autenticacao e autorizacao para todos os sistemas do ecossistema CARF. Implementa OAuth2 e OpenID Connect fornecendo single sign-on entre aplicacoes web, mobile e desktop.

Configurado com single realm CARF contendo todos os usuarios e clients. Multi-tenancy implementado via atributos de usuario (tenants, current_tenant, community_ids) mapeados como claims customizados no JWT pelo scope carf-tenant. Hierarquia de 6 roles em arvore define permissoes desde cadastrador de campo ate super-administrador de plataforma. Temas customizados com Keycloakify reutilizando componentes @carf/ui.

## Capacidades

Fluxos OAuth2 diferenciados por tipo de client: Authorization Code com PKCE para web e mobile, Client Credentials para backend-to-backend (geogis). Validacao de CPF customizada no formulario de login via hook @carf/ui e SPI Java servidor-side. Registro de usuarios desabilitado (usuarios criados via ADMIN). Politica de senha realm-wide com minimo 8 caracteres. Session management com access token de 5 minutos, SSO idle 30 minutos e SSO max 10 horas. Detalhes tecnicos no repositorio carf-keycloak.
