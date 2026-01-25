---
id: UC-P3-001
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
---

# UC-P3-001: Autenticar Agente de Campo

Autenticacao do Agente de Campo no app REURBCAD via Keycloak.

## Referencia

Este UC implementa passo 11 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo.md).

## Atores

- Primario: Agente de Campo
- Secundario: Keycloak, Backend GEOAPI

## Pre-condicoes

- Agente de Campo possui credenciais validas no Keycloak
- Agente de Campo esta designado a um TENANT
- App REURBCAD instalado no dispositivo mobile
- Analista JA PUBLICOU trabalho do TENANT (PARTE 2 concluida)

## Fluxo Principal

1. Agente de Campo abre o app REURBCAD
2. App verifica se ha sessao salva
3. Se nao ha sessao, app exibe tela de login
4. App inicia fluxo OAuth2 PKCE
5. Sistema redireciona para Keycloak
6. Agente insere credenciais (usuario/senha)
7. Keycloak valida credenciais
8. Keycloak emite token JWT com `tenant_id`
9. App recebe e armazena tokens de forma segura
10. App verifica designacao ao TENANT
11. App sincroniza dados iniciais do TENANT
12. Sessao iniciada com sucesso

## Fluxos Alternativos

- FA-001: Login biometrico (se configurado)
- FA-002: Sessao existente valida (skip login)

## Fluxos de Excecao

- FE-001: Credenciais invalidas
- FE-002: Usuario nao designado a TENANT
- FE-003: Token expirado (reautenticar)
- FE-004: Sem conexao para autenticar

## Pos-condicoes

- Sessao autenticada no app
- Token JWT armazenado de forma segura
- TENANT do agente identificado
- Agente pode baixar pacote (UC-P3-002)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Autenticacao via Keycloak e OBRIGATORIA |
| RN-02 | Agente so acessa dados APOS autenticar |
| RN-03 | Token contem tenant_id do agente |
