---
type: leaf
status: review
updated: 2026-02-07
---

# Tratamento de Erros

Especificacao do tratamento de erros no WEBDOCS, cobrindo erros de autenticacao e API.

## Erros de Autenticacao

| Erro | Deteccao | Acao | Mensagem |
|------|----------|------|----------|
| Token expirado | JWT exp menor que timestamp atual | Refresh silencioso. Se falha, redirect para login | Sua sessao expirou. |
| Token invalido | JWT malformado ou assinatura invalida | Limpar cookies, redirect para login | Erro de autenticacao. |
| Token ausente | Cookie access_token ausente | Redirect para /auth/login com return_url | Voce precisa fazer login. |
| Role insuficiente | Nenhuma role permite acesso | Renderizar pagina 403 | Voce nao tem permissao. |
| Keycloak indisponivel | Timeout ou erro de rede | Pagina de erro com retry | Servico temporariamente indisponivel. |
| Erro OAuth | Keycloak retorna error param | Pagina de erro com descricao | Erro durante autenticacao. |

Erros comuns de OAuth: access_denied (negado pelo admin), invalid_scope (escopo nao permitido), server_error (erro interno).

## Erros de API (GeoAPI)

| Erro | Deteccao | Acao | Mensagem |
|------|----------|------|----------|
| Erro de rede | fetch throws TypeError/AbortError | Botao retry | Nao foi possivel conectar. |
| Timeout | AbortController apos 10s | Botao retry | Requisicao demorou muito. |
| Erro 5xx | Status 500-599 | Log error com request_id | Erro interno do servidor. |
| Not Found 404 | Status 404 | Mensagem especifica | Recurso nao encontrado. |
| Unauthorized 401 | Status 401 | Tentar refresh, senao login | Sessao invalida. |
| Forbidden 403 | Status 403 | Mensagem de permissao | Sem permissao para operacao. |
| Validacao 400 | Status 400 com body | Erros especificos | Dados invalidos: {field}. |

Erros de conteudo, paginas customizadas, logging e error boundaries estao em 11-error-handling-detalhes.md.
