---
type: leaf
status: review
updated: 2026-02-08
---

# Admin Security

Os endpoints /api/admin da GEOAPI implementam 7 camadas de seguranca para proteger operacoes administrativas sensiveis de gerenciamento de tenants, usuarios, roles e configuracoes, consumidas pelo console REURBMASTER.

## Decisao Arquitetural

A decisao de usar SPA React Vite com PKCE flow conectando ao backend .NET foi motivada por seguranca. API Routes de frameworks SSR com Keycloak Admin Client requerem client_secret confidencial que pode vazar no bundle client-side. A solucao segura isola o client_secret no backend .NET onde os endpoints /api/admin usam Keycloak Admin Client com client credentials flow, nunca expondo credenciais ao frontend.

## Fluxo de Requisicao

O fluxo inicia quando o REURBMASTER SPA envia POST /api/admin/users com Bearer JWT. O AdminController com Authorize(Roles = "admin, super-admin") valida o token e a role. O handler via MediatR processa o command com FluentValidation. O KeycloakAdminService usa client_secret confidencial para comunicar com a Keycloak Admin REST API. O response retorna ao ADMIN com auditoria registrada automaticamente pelo AuditLoggingBehavior.

## Sete Camadas de Seguranca

A primeira e autenticacao OAuth2 com JWT do Keycloak validado pelo middleware. A segunda e autorizacao RBAC com roles admin e super-admin verificadas via policies. A terceira e isolamento por tenant onde admin ve apenas seu proprio tenant via RLS. A quarta e validacao de entrada via FluentValidation sanitizando DTOs. A quinta e rate limiting protegendo endpoints sensiveis contra forca bruta. A sexta e auditoria completa com todas as acoes admin registradas em audit_logs com IP, usuario e timestamp. A setima e criptografia com TLS 1.3 em transito e secrets criptografados em repouso.

## Escopo de Acesso

O admin acessa apenas usuarios do proprio tenant. O super-admin acessa todos os tenants, pode criar novos tenants e transferir usuarios. Demais roles nao tem acesso a endpoints admin.
