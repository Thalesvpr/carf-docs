---
type: readme
status: approved
updated: 2026-01-25
---

# Integracoes WMS/WMTS

Requisitos funcionais para integracao de servicos de mapas externos no ecossistema CARF. Suporta adicao de camadas WMS e WMTS de orgaos governamentais e provedores de dados geoespaciais, com proxy para resolver problemas de CORS e cache de tiles.

Os requisitos [RF-212](./RF-212-adicionar-camada-wms.md) a [RF-217](./RF-217-excluir-camada-wmswmts.md) cobrem ciclo de vida completo de camadas WMS/WMTS incluindo adicao, teste de conexao, listagem, edicao e exclusao com soft delete. Os requisitos [RF-218](./RF-218-ordenação-de-camadas-base.md) a [RF-220](./RF-220-trocar-basemap.md) tratam ordenacao de camadas, basemaps padrao (OpenStreetMap, Google Satellite) e selecao pelo usuario. O requisito [RF-221](./RF-221-proxy-de-wmswmts.md) implementa proxy na GEOAPI para resolver CORS e cache de tiles.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (10)

| Documento | Status |
|-----------|--------|
| [RF-212: Adicionar Camada WMS](./RF-212-adicionar-camada-wms.md) | ⚠ |
| [RF-213: Adicionar Camada WMTS](./RF-213-adicionar-camada-wmts.md) | ⚠ |
| [RF-214: Testar Conexao WMS/WMTS](./RF-214-testar-conexão-wmswmts.md) | ⚠ |
| [RF-215: Listar Camadas WMS/WMTS](./RF-215-listar-camadas-wmswmts.md) | ⚠ |
| [RF-216: Editar Camada WMS/WMTS](./RF-216-editar-camada-wmswmts.md) | ⚠ |
| [RF-217: Excluir Camada WMS/WMTS](./RF-217-excluir-camada-wmswmts.md) | ⚠ |
| [RF-218: Ordenacao de Camadas Base](./RF-218-ordenação-de-camadas-base.md) | ⚠ |
| [RF-219: Basemaps Padrao](./RF-219-basemaps-padrão.md) | ⚠ |
| [RF-220: Trocar Basemap](./RF-220-trocar-basemap.md) | ⚠ |
| [RF-221: Proxy de WMS/WMTS](./RF-221-proxy-de-wmswmts.md) | ⚠ |

<!-- CARF-INDEX-END -->
