---
type: leaf
status: review
updated: 2026-02-07
---

# Error Codes - HTTP e Mensagens de Autenticacao

Codigos HTTP retornados pela Admin REST API e mensagens de erro na tela de login.

## Codigos HTTP de Sucesso

| Codigo | Descricao | Uso |
|:-------|:----------|:----|
| 200 OK | Operacao bem-sucedida | GET, POST token |
| 201 Created | Recurso criado, header Location | POST criacao |
| 204 No Content | Sem corpo de resposta | DELETE, PUT |

## Codigos HTTP de Erro do Cliente

| Codigo | Descricao | Acao |
|:-------|:----------|:-----|
| 400 Bad Request | Request invalido | Validar payload |
| 401 Unauthorized | Token invalido ou ausente | Refresh ou re-autenticar |
| 403 Forbidden | Sem permissao | Verificar roles |
| 404 Not Found | Recurso inexistente | Verificar ID |
| 409 Conflict | Username ou email duplicado | Usar valor unico |
| 429 Too Many Requests | Rate limit | Backoff exponencial |

## Codigos HTTP de Erro do Servidor

| Codigo | Descricao | Acao |
|:-------|:----------|:-----|
| 500 Internal Server Error | Erro interno | Verificar logs |
| 503 Service Unavailable | Servidor sobrecarregado | Retry com backoff |

## Mensagens de Autenticacao

Mensagens na tela de login, internacionalizaveis via messages_*.properties.

| Chave | Mensagem pt-BR | Causa |
|:------|:---------------|:------|
| invalidUserMessage | Usuario ou senha invalidos | Login falhou |
| accountDisabledMessage | Conta desabilitada | enabled false |
| accountTemporarilyDisabledMessage | Conta bloqueada | Brute force |
| expiredCodeMessage | Codigo expirado | Auth code timeout |
| sessionExpiredMessage | Sessao expirada | SSO timeout |
| invalidEmailMessage | Email invalido | Validacao |
| missingPasswordMessage | Senha nao informada | Campo vazio |
| notMatchPasswordMessage | Senhas nao conferem | Registro/reset |

## Tratamento no Frontend

O frontend deve inspecionar o campo error. Para invalid_grant redirecionar para login. Para access_denied informar falta de permissao. Para invalid_client logar e orientar contato com suporte. Para invalid_scope logar como warning. Demais erros exibem error_description ou mensagem generica.

Ver [07-error-codes](./07-error-codes.md) para erros OAuth2 RFC 6749.
