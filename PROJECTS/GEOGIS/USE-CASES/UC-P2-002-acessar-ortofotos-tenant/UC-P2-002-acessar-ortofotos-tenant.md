---
id: UC-P2-002
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-2
---

# UC-P2-002: Acessar Ortofotos do Tenant

Analista acessa catalogo de ortofotos disponiveis para seu TENANT.

## Referencia

Este UC implementa passo 7 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/02-georreferenciamento.md).

## Atores

- Primario: Analista (Plugin QGIS)
- Secundario: Backend GEOAPI, Bucket S3/MinIO

## Pre-condicoes

- Analista autenticado (UC-P2-001 concluido)
- Ortofotos disponiveis para o TENANT (PARTE 1 concluida)

## Fluxo Principal

1. Plugin consulta backend: `GET /api/ortofotos?tenant_id={tenant}`
2. Backend valida token e extrai tenant_id
3. Backend retorna lista de ortofotos do TENANT
4. Plugin exibe lista/catalogo de ortofotos disponiveis
5. Analista visualiza informacoes de cada ortofoto:
   - Data de captura
   - Area coberta
   - Resolucao
   - Status (nova, em uso, finalizada)
6. Analista seleciona ortofoto desejada
7. Plugin solicita acesso ao backend
8. Backend gera URL presigned temporaria
9. Plugin carrega ortofoto como camada raster (WMS/WMTS ou download)
10. Ortofoto exibida no canvas do QGIS

## Fluxos Alternativos

- FA-001: Carregar via WMS/WMTS (streaming)
- FA-002: Download direto para uso offline

## Fluxos de Excecao

- FE-001: Nenhuma ortofoto disponivel para o TENANT
- FE-002: Falha ao carregar ortofoto (conexao)
- FE-003: URL presigned expirada

## Pos-condicoes

- Ortofoto carregada no QGIS
- Analista pode iniciar georreferenciamento (UC-P2-003)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Analista SO acessa ortofotos do TENANT designado |
| RN-02 | URLs presigned expiram apos periodo curto |
| RN-03 | Acesso a ortofotos e registrado em audit log |
