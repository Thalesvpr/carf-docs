---
type: leaf
status: review
updated: 2026-02-07
---

# Error Codes - Erros OAuth2

Codigos de erro OAuth2 retornados pelo Keycloak seguindo RFC 6749. Respostas contem campos error e error_description.

## invalid_request

Request malformado ou faltando parametros.

| Contexto | Causa | Solucao |
|:---------|:------|:--------|
| Authorization | client_id ou redirect_uri ausente | Verificar URL |
| Token | grant_type ou code ausente | Verificar payload |
| Token | redirect_uri diferente | Usar mesma redirect_uri |

## invalid_client

| Causa | Solucao |
|:------|:--------|
| client_id inexistente | Verificar no Admin Console |
| client_secret incorreto | Regenerar secret |
| Client desabilitado | Habilitar no Admin Console |
| Autenticacao faltando | Incluir client_id e secret |

## invalid_grant

Authorization code ou refresh token invalido.

| Causa | Solucao |
|:------|:--------|
| Code expirado (60s) | Trocar code imediatamente |
| Code ja usado | Codes sao single-use |
| Refresh token expirado | Re-autenticar |
| PKCE code_verifier incorreto | Verificar geracao |

## unauthorized_client

| Causa | Solucao |
|:------|:--------|
| Client credentials em publico | Converter para confidencial |
| Auth code flow desabilitado | Habilitar standardFlowEnabled |
| Direct access desabilitado | Habilitar directAccessGrantsEnabled |

## unsupported_grant_type

| Grant Type | Configuracao |
|:-----------|:-------------|
| authorization_code | standardFlowEnabled true |
| refresh_token | Automatico com auth code |
| client_credentials | serviceAccountsEnabled true |
| password | directAccessGrantsEnabled true |

## invalid_scope

Scope inexistente ou nao atribuido ao client como default ou optional scope.

## access_denied

Usuario cancelou consent, conta desabilitada, brute force lock ou required action pendente.

## server_error e temporarily_unavailable

Erro interno indica problemas de database ou configuracao. Servidor indisponivel exige retry com backoff.

Ver [07a-error-codes-http](./07a-error-codes-http.md) para codigos HTTP e mensagens de autenticacao.
