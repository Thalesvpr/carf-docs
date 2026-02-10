---
type: workflow
status: approved
updated: 2026-02-07
part: 2
step: 6
---

# Passo 6: Autenticacao no Plugin

Autenticacao dupla do Analista no Plugin GEOGIS (Keycloak + AUTHENTICATION KEY).

## Fluxo

1. Analista abre o QGIS
2. Analista ativa o Plugin GEOGIS
3. Plugin exibe tela de login
4. Autenticacao dupla obrigatoria: primeiro login via Keycloak (OAuth2 PKCE desktop flow), depois informar AUTHENTICATION KEY (chave adicional do plugin)
5. Plugin valida ambas credenciais contra o backend
6. Plugin armazena tokens de forma segura (QSettings encrypted)
7. Sessao iniciada com sucesso

## Autenticacao Dupla

No passo 6.1, o plugin redireciona para a pagina de login do Keycloak. O Analista insere usuario e senha, e o Keycloak emite um token JWT que retorna ao plugin. No passo 6.2, o plugin solicita a AUTHENTICATION KEY. O Analista insere a chave e o plugin valida contra o backend.

## AUTHENTICATION KEY

A AUTHENTICATION KEY e diferente do login Keycloak. Formato e string alfanumerica (ex: carf_key_abc123xyz789). Pode ser revogada independentemente do usuario, adiciona camada extra de seguranca e vincula a sessao/ambiente ao backend.

## Armazenamento Seguro

O Plugin armazena credenciais de forma segura: tokens em QSettings criptografado, AUTHENTICATION KEY encriptada e renovacao automatica de tokens.

## Resultado

- Analista autenticado no Plugin
- Tokens Keycloak armazenados
- AUTHENTICATION KEY validada
- Sessao ativa para operacoes

## Proximo Passo

Passo 7: Acesso as Ortofotos
