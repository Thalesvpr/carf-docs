---
type: leaf
status: review
updated: 2026-01-19
---

# Validação de Token

GEOAPI valida access token em cada requisição usando middleware JWT Bearer Authentication do ASP.NET Core. Configuração em Program.cs adiciona autenticação com parâmetros do Keycloak: Authority (URL do realm), Audience (client_id carf-geoapi), RequireHttpsMetadata true em produção.

Validação automática verifica assinatura RS256 usando chave pública obtida de JWKS endpoint (/.well-known/openid-configuration). Middleware cacheia JWKS por 24 horas reduzindo chamadas ao Keycloak. Claims exp e nbf validados contra relógio do servidor com tolerância de 5 minutos para clock skew.

Após validação de assinatura, TenantMiddleware customizado extrai claim tenant_id e configura variável de sessão PostgreSQL via SET app.tenant_id. Todas as queries subsequentes filtradas automaticamente por RLS policies usando current_setting('app.tenant_id').

Validação de roles ocorre em dois níveis: atributo [Authorize(Roles = "analyst")] em controllers bloqueia acesso se role ausente, e verificação programática User.IsInRole("admin") permite lógica condicional dentro de actions.

Token inválido (assinatura incorreta, expirado, audience errado) resulta em 401 Unauthorized. Token válido mas sem role necessária resulta em 403 Forbidden. Ambos os casos logados para auditoria com IP do cliente e endpoint acessado.
