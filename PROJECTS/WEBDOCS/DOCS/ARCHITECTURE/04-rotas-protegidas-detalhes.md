---
type: leaf
status: review
updated: 2026-02-07
---

# Rotas Protegidas - Detalhes de Implementacao

Detalhes tecnicos da implementacao do middleware de rotas protegidas. Documento complementar a 04-rotas-protegidas.md.

## Cookies Esperados

| Cookie | httpOnly | secure | sameSite | path | Descricao |
|--------|----------|--------|----------|------|-----------|
| access_token | Sim | Sim | Lax | / | JWT de acesso para autenticacao |
| refresh_token | Sim | Sim | Lax | /auth | Token para renovacao do access_token |

O cookie access_token e enviado em todas requisicoes enquanto refresh_token e enviado apenas para rotas /auth/ minimizando exposicao.

## Tratamento de Erros

Usuario nao autenticado recebe redirect 302 para /auth/login?redirect=url_atual preservando destino original. Apos login, callback redireciona para URL preservada.

Usuario autenticado sem permissao recebe pagina 403 customizada com explicacao de que secao requer permissao especifica, lista das roles necessarias, e link para logout ou home.

Token expirado dispara tentativa de refresh silencioso antes de qualquer resposta de erro. Sucesso e transparente ao usuario. Falha resulta em redirect para login.

## Performance

Validacao de assinatura JWT usa chave publica do Keycloak JWKS endpoint. Cache da chave mantido por 24 horas ou ate falha de validacao indicando possivel rotacao. Decodificacao no edge nao valida assinatura para reduzir latencia, confiando no httpOnly do cookie.

## Implementacao do Middleware

Middleware reside em src/middleware.ts e exporta onRequest do tipo MiddlewareHandler de astro:middleware. Utiliza funcao sequence para composicao de middlewares.

### Astro Locals

O middleware popula Astro.locals com informacoes do usuario autenticado. Interface Locals no namespace App define campo user (contendo id, email, name, roles como array de strings, e tenantId como string ou null), campo isAuthenticated como boolean, e campo opcional allowedRoles populado em caso de 403.

### Dependencia jose

Pacote jose versao 5.2.0 ou superior, instalado via bun add jose, fornece funcionalidade de JWT verification com JWKS.
