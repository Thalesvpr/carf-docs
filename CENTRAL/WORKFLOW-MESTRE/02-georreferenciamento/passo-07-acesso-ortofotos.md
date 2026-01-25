---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 7
---

# Passo 7: Acesso as Ortofotos do TENANT

Analista acessa e carrega ortofotos disponiveis no TENANT.

## Fluxo

1. Plugin consulta backend: `GET /api/ortofotos?tenant_id={tenant}`
2. Backend retorna lista de ortofotos disponiveis para o TENANT
3. Plugin exibe lista/catalogo de ortofotos
4. Analista seleciona ortofoto desejada
5. Plugin carrega ortofoto como camada raster (WMS/WMTS ou download direto)
6. Ortofoto exibida no canvas do QGIS

## API Request

```http
GET /api/ortofotos?tenant_id={tenant}
Authorization: Bearer {jwt_token}
X-Auth-Key: {authentication_key}
```

## Response

```json
{
  "ortofotos": [
    {
      "id": "uuid",
      "nome": "Ortofoto Comunidade X",
      "data_captura": "2026-01-15",
      "bbox": [-43.2, -22.9, -43.1, -22.8],
      "url_wmts": "https://...",
      "url_download": "https://..."
    }
  ]
}
```

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
