---
type: workflow
status: approved
updated: 2026-02-07
part: 2
step: 7
---

# Passo 7: Acesso as Ortofotos do TENANT

Analista acessa e carrega ortofotos disponiveis no TENANT.

## Fluxo

1. Plugin consulta backend via requisicao GET para /api/ortofotos com parametro tenant_id, enviando Bearer token e AUTHENTICATION KEY nos headers
2. Backend retorna lista de ortofotos disponiveis para o TENANT
3. Plugin exibe lista/catalogo de ortofotos
4. Analista seleciona ortofoto desejada
5. Plugin carrega ortofoto como camada raster (WMS/WMTS ou download direto)
6. Ortofoto exibida no canvas do QGIS

## Dados da Resposta

Cada ortofoto retornada inclui os seguintes campos:

| Campo | Descricao |
|-------|-----------|
| id | UUID da ortofoto |
| nome | Nome descritivo |
| data_captura | Data de captura pelo drone |
| bbox | Bounding box com coordenadas |
| url_wmts | URL para streaming via protocolo OGC |
| url_download | URL para download do arquivo completo |

## Modos de Carregamento

| Modo | Descricao | Uso |
|------|-----------|-----|
| WMS/WMTS | Streaming via protocolo OGC | Visualizacao rapida |
| Download | Arquivo completo local | Trabalho offline |

## Resultado

- Lista de ortofotos exibida no Plugin
- Ortofoto selecionada carregada no QGIS
- Camada raster pronta para georreferenciamento

## Proximo Passo

Passo 8: Georreferenciamento
