---
id: UC-P1-001
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-02-21
workflow: PARTE-1
---

# UC-P1-001: Entregar Ortofoto

Fluxo de entrega de ortofoto pelo Operador de Drone ao sistema.

## Referencia

Este UC implementa passos 1-2 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos.md).

## Atores

- Primario: Operador de Drone
- Secundario: Keycloak, Backend GEOAPI

## Pre-condicoes

- Operador de Drone possui credenciais validas no Keycloak
- Operador de Drone esta designado a um TENANT
- Ortofoto esta pronta para envio (mosaico processado)
- Backend esta operacional

## Fluxo Principal

1. Operador de Drone recebe link/portal para envio de ortofotos
2. Operador acessa o portal de upload
3. Sistema redireciona para Keycloak
4. Operador insere credenciais (usuario/senha)
5. Keycloak valida credenciais e emite token JWT
6. Token contem `tenant_id` do operador
7. Sistema redireciona de volta ao portal
8. Operador seleciona arquivo de ortofoto
9. Sistema valida formato (GeoTIFF, JPEG2000)
10. Sistema valida tamanho maximo permitido
11. Sistema inicia upload multipart
12. Progresso e exibido ao usuario
13. Upload concluido com sucesso
14. Sistema aciona processamento (UC-P1-002)

## Fluxos de Excecao

- FE-001: Formato de arquivo invalido
- FE-002: Tamanho excede limite
- FE-003: Falha no upload (conexao)
- FE-004: Token expirado durante upload

## Pos-condicoes

- Ortofoto recebida pelo backend
- Processamento iniciado (UC-P1-002)
- Registro de entrega no audit log

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Autenticacao via Keycloak e OBRIGATORIA |
| RN-02 | Apenas Operadores de Drone (role `drone-operator`) podem enviar ortofotos |
| RN-03 | Ortofoto deve ter coordenadas embarcadas |
