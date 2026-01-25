---
id: UC-P1-003
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-1
---

# UC-P1-003: Disponibilizar Ortofoto para Tenant

Armazenamento da ortofoto em bucket segregado por tenant, tornando-a disponivel para analistas.

## Referencia

Este UC implementa passo 4 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos.md).

## Atores

- Primario: Backend GEOAPI (automatico)
- Secundario: Bucket S3/MinIO

## Pre-condicoes

- Ortofoto processada (UC-P1-002 concluido)
- Tenant do Analista de Drone identificado
- Bucket operacional

## Fluxo Principal

1. Backend determina TENANT do Analista de Drone (via token JWT)
2. Backend cria estrutura de pastas no bucket:
   - `/{tenant_id}/ortofotos/{ano}/{mes}/`
3. Backend salva arquivos:
   - `original/` - ortofoto original
   - `otimizada/` - versao reduzida
   - `tiles/` - tiles para visualizacao
4. Backend registra URLs no banco de dados
5. Backend associa ortofoto ao TENANT
6. Backend marca ortofoto como "disponivel"
7. Analistas do mesmo TENANT podem acessar (PARTE 2)

## Fluxos de Excecao

- FE-001: Falha ao criar estrutura no bucket
- FE-002: Falha ao copiar arquivos
- FE-003: Tenant invalido ou inativo

## Pos-condicoes

- Ortofoto armazenada no bucket do tenant
- URLs registradas no banco
- Ortofoto associada ao TENANT correto
- Analistas (Plugin QGIS) podem acessar

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Ortofoto SEMPRE e salva em bucket (S3/MinIO) |
| RN-02 | Ortofoto SEMPRE e associada ao TENANT do analista |
| RN-03 | Apenas usuarios do mesmo TENANT podem acessar |
| RN-04 | Segregacao por tenant e OBRIGATORIA |
