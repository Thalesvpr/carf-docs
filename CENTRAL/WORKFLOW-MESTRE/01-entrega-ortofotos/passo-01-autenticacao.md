---
type: workflow
status: approved
updated: 2026-02-21
part: 1
step: 1
---

# Passo 1: Autenticacao

Autenticacao do Operador de Drone no sistema via Keycloak.

## Fluxo

1. Um Manager gera o link de upload no ReurbWeb, vinculando-o a uma comunidade/regiao especifica do TENANT
2. O Manager compartilha o link com o Operador de Drone (por e-mail, mensagem, etc.)
3. Operador de Drone acessa o link recebido
4. Sistema redireciona para Keycloak
5. Operador de Drone insere credenciais (usuario/senha)
6. Keycloak valida credenciais e emite token JWT
7. Token contem tenant_id do operador
8. Sistema redireciona de volta ao portal de upload

## Fluxo de Autenticacao

O Manager gera um link de upload no ReurbWeb associado a uma comunidade/regiao especifica. Esse link e compartilhado com o Operador de Drone, que o acessa e e redirecionado para a pagina de login do Keycloak. Apos validacao de credenciais, o Keycloak emite um token JWT contendo o tenant_id e redireciona de volta ao portal de upload com a sessao autenticada.

## Resultado

- Operador de Drone autenticado
- Token JWT valido com tenant_id
- Acesso ao portal de upload liberado

## Proximo Passo

Passo 2: Upload da Ortofoto
