---
id: UC-P3-002
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-3
---

# UC-P3-002: Download do Pacote Temporario

Agente de Campo baixa pacote unico e temporario com dados para operacao offline.

## Referencia

Este UC implementa passo 12 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo.md).

## Atores

- Primario: Agente de Campo
- Secundario: Backend GEOAPI, Bucket S3/MinIO

## Pre-condicoes

- Agente autenticado (UC-P3-001 concluido)
- Analista JA PUBLICOU trabalho do TENANT
- Conexao com internet disponivel

## Fluxo Principal

1. App consulta backend: `GET /api/pacotes/campo?tenant_id={tenant}`
2. Backend verifica:
   - Agente pertence ao TENANT
   - Analista JA PUBLICOU trabalho do TENANT
3. **SOMENTE SE PUBLICADO:** Backend prepara pacote contendo:
   - Ortofoto (versao para uso offline)
   - Poligonos georreferenciados (comunidades/quadras/lotes)
   - Metadados necessarios
4. Backend gera URL presigned UNICA e TEMPORARIA
5. App inicia download do pacote
6. Progresso exibido ao usuario
7. Download concluido
8. App armazena pacote localmente (WatermelonDB)
9. URL expira apos uso (download unico)
10. App marca pacote como "disponivel offline"

## Fluxos de Excecao

- FE-001: Nenhum trabalho publicado para o TENANT
- FE-002: Falha no download (conexao)
- FE-003: Espaco insuficiente no dispositivo
- FE-004: URL expirada (solicitar nova)

## Pos-condicoes

- Pacote armazenado localmente
- Dados disponiveis para operacao offline
- Agente pode selecionar comunidade (UC-P3-003)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Agente SO baixa dados APOS publicacao do Analista |
| RN-02 | Download e UNICO e TEMPORARIO |
| RN-03 | URL presigned expira apos uso |
| RN-04 | Dados NAO ficam disponiveis ANTES da publicacao |
