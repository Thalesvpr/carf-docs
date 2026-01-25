---
id: UC-P2-001
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-2
---

# UC-P2-001: Autenticar no Plugin QGIS

Autenticacao dupla do Analista no Plugin GEOGIS: Keycloak + Authentication Key.

## Referencia

Este UC implementa passos 5-6 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/02-georreferenciamento.md).

## Atores

- Primario: Analista (Plugin QGIS)
- Secundario: Keycloak, Backend GEOAPI

## Pre-condicoes

- Analista possui credenciais validas no Keycloak
- Analista esta designado a um TENANT
- Plugin GEOGIS instalado no QGIS
- Analista possui AUTHENTICATION KEY valida

## Fluxo Principal

1. Analista abre o QGIS
2. Analista ativa o Plugin GEOGIS
3. Plugin exibe tela de login
4. **Autenticacao dupla obrigatoria:**
5. Analista inicia login via Keycloak (OAuth2 PKCE desktop flow)
6. Keycloak valida credenciais e emite token JWT
7. Token contem `tenant_id` do analista
8. Plugin solicita AUTHENTICATION KEY
9. Analista insere AUTHENTICATION KEY
10. Plugin valida key contra o backend
11. Backend verifica se key e valida e associada ao usuario
12. Plugin armazena tokens de forma segura (QSettings encrypted)
13. Sessao iniciada com sucesso

## Fluxos de Excecao

- FE-001: Credenciais Keycloak invalidas
- FE-002: AUTHENTICATION KEY invalida ou revogada
- FE-003: Usuario nao designado a nenhum TENANT
- FE-004: Token expirado

## Pos-condicoes

- Sessao autenticada no plugin
- Token JWT armazenado de forma segura
- AUTHENTICATION KEY validada
- Analista pode acessar ortofotos (UC-P2-002)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Plugin exige Keycloak + AUTHENTICATION KEY |
| RN-02 | AUTHENTICATION KEY e ADICIONAL ao Keycloak |
| RN-03 | Key pode ser revogada independentemente do usuario |
| RN-04 | Tokens armazenados criptografados |
