---
type: leaf
status: review
updated: 2026-02-07
---

# Configurar Autenticacao

Guia para configurar integracao com Keycloak habilitando protecao da secao /dev/ e autenticacao do CMS.

## Variaveis de Ambiente

| Variavel | Desenvolvimento | Producao |
|---|---|---|
| KEYCLOAK_URL | http://localhost:8080 | https://auth.carf.com.br |
| KEYCLOAK_REALM | carf | carf |
| KEYCLOAK_CLIENT_ID | carf-webdocs | carf-webdocs |

Obter credenciais com equipe de infraestrutura. Configurar variaveis em arquivo .env.local para desenvolvimento.

## Configuracao do Client no Keycloak

Acessar Keycloak Admin Console, selecionar Realm "carf", navegar para Clients e selecionar carf-webdocs. Verificar as seguintes configuracoes:

| Propriedade | Valor |
|---|---|
| Client Protocol | openid-connect |
| Access Type | public |
| Standard Flow Enabled | true |
| Direct Access Grants Enabled | false |
| PKCE Code Challenge Method | S256 |
| Valid Redirect URIs | http://localhost:4321/auth/callback e https://docs.carf.com.br/auth/callback |
| Web Origins | http://localhost:4321 e https://docs.carf.com.br |

## Fluxo de Teste

| Passo | Acao | Resultado Esperado |
|---|---|---|
| 1 | Acessar http://localhost:4321/dev/ | Redirect para Keycloak login |
| 2 | Fazer login com credenciais dev | Redirect de volta para /dev/ |
| 3 | Verificar cookie no DevTools | carf_access_token presente |
| 4 | Acessar /auth/logout | Redirect para Keycloak logout, depois home |
| 5 | Acessar /dev/ novamente | Redirect para login (nao autenticado) |

## Debug de JWT

Para inspecionar token JWT, abrir DevTools, navegar para Application e Cookies, copiar valor de carf_access_token e colar em jwt.io. Verificar que realm_access.roles contem roles do usuario, exp e futuro, e iss e URL do Keycloak.

## Troubleshooting

| Erro | Causa | Solucao |
|---|---|---|
| Invalid parameter: redirect_uri | URI nao autorizada | Adicionar URI exata em Valid Redirect URIs do client |
| Access-Control-Allow-Origin not present | Origem nao configurada | Adicionar origem em Web Origins do client |
| Too many redirects | Cookie nao salvo | Verificar SameSite=Lax e Secure correto para ambiente |
| 403 mesmo logado | Role ausente | Keycloak, Users, Role Mappings, adicionar role dev |
| 401 apos minutos | Token expirado | Verificar refresh_token cookie e endpoint /auth/refresh |
