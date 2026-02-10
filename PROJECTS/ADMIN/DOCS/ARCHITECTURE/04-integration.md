---
type: leaf
status: review
updated: 2026-02-07
---

# Integration - ADMIN

## Integracoes

O ADMIN integra-se com quatro sistemas principais. A integracao com GEOAPI acontece via @carf/geoapi-client consumindo endpoints /api/admin/ protegidos por role check no backend, incluindo POST /api/admin/users, DELETE /api/admin/tenants e GET /api/admin/audit-logs. O GEOAPI faz proxy seguro para Keycloak Admin API mantendo client_secret confidencial no backend. A integracao com @carf/tscore fornece KeycloakClient para auth com PKCE flow sem client_secret no frontend, alem de validacoes de CPF, CNPJ e Email e types compartilhados. O shadcn/ui fornece componentes visuais como DataTable, Dialog e Form. O React Router implementa protected routes validando role antes de renderizar paginas admin, redirecionando para /unauthorized se o usuario nao tem permissao.

## Mapa de Integracoes

| Sistema | Protocolo | Funcao |
|---------|-----------|--------|
| GEOAPI /api/admin/ | HTTPS + JWT Bearer | Proxy seguro para operacoes administrativas |
| Keycloak Admin API | Via GEOAPI com client_secret | Gerenciamento de usuarios e roles |
| @carf/tscore | Dependencia NPM | Auth PKCE, validacoes, types |
| shadcn/ui | Dependencia NPM | Componentes visuais |
| React Router v6 | Client-side | Rotas protegidas com validacao de role |

## Arquitetura de Seguranca

O fluxo de seguranca segue uma cadeia de confianca onde o ADMIN SPA nao possui nenhum secret, autenticando-se via PKCE flow diretamente com o Keycloak. O JWT obtido e enviado ao GEOAPI nos endpoints /api/admin/ que verificam a role do usuario. Somente o GEOAPI possui o client_secret confidencial necessario para acessar a Keycloak Admin API e executar operacoes de gerenciamento de usuarios e roles. Essa separacao garante que credenciais sensiveis nunca ficam expostas no frontend.
