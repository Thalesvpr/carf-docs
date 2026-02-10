---
type: leaf
status: review
updated: 2026-02-07
---

# PKCE Implementation - Visao Geral

PKCE protege contra interceptacao de codigo de autorizacao. Obrigatorio para public clients como WEBDOCS. Relacionado com 21b-pkce-flows.md e 21c-pkce-security.md.

## Fluxo

Gera code_verifier (string aleatoria salva em cookie httpOnly). Gera code_challenge (SHA256 do verifier base64url) enviado ao authorization endpoint. Usuario autentica no Keycloak que redireciona com code. Troca code por tokens enviando code + code_verifier, Keycloak verifica SHA256(verifier) == challenge.

## Code Verifier

| Propriedade | Valor |
|-------------|-------|
| Charset | A-Z, a-z, 0-9, -, ., _, ~ |
| Minimo/Maximo/Recomendado | 43 / 128 / 64 chars |

Implementacao em src/lib/auth/pkce.ts usa crypto.getRandomValues com Uint8Array de 64 bytes mapeados para charset via modulo.

## Code Challenge

Metodo S256 obrigatorio. Converter verifier para UTF-8 via TextEncoder, calcular SHA-256 com crypto.subtle.digest, converter para base64 com btoa, substituir + por -, / por _, remover =. Funcao generateCodeChallenge retorna Promise de string.

## Storage

Cookie carf_auth_state com httpOnly true, secure true, sameSite Lax, path /auth, maxAge 600s. Payload JSON com state (CSRF), code_verifier, redirect_to e created_at. Encoding base64url sem criptografia. Funcao generateState cria 32 bytes hex. Funcao createAuthStateCookie retorna cookie string, state e codeChallenge.
