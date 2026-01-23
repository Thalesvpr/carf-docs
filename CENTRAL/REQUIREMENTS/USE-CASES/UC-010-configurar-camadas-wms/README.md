---
type: readme
status: approved
updated: 2026-01-23
---

# UC-010: Configurar Camadas WMS/WMTS

Caso de uso para adicionar servidores WMS e WMTS externos como camadas base no mapa do sistema. O fluxo envolve ADMIN configurando URL do servico, testando conexao, selecionando layers disponiveis e ajustando parametros de exibicao.

O [fluxo principal](./UC-010-configurar-camadas-wms.md) documenta a configuracao de camadas WMS. Os fluxos alternativos cobrem adicao de WMTS com tiles pre-renderizados (FA-001) e uso de proxy para evitar bloqueios CORS (FA-002). Os fluxos de excecao tratam falha no GetCapabilities (FE-001), XML invalido (FE-002), layer nao encontrado (FE-003) e erro ao renderizar no frontend (FE-004).


<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (7)

| Documento | Status |
|-----------|--------|
| [UC-010: Configurar Camadas WMS/WMTS](./UC-010-configurar-camadas-wms.md) | ⚠ |
| [UC-010-FA-001: Adicionar WMTS](./UC-010-FA-001-adicionar-wmts.md) | ⚠ |
| [UC-010-FA-002: Proxy de WMS](./UC-010-FA-002-proxy-wms.md) | ⚠ |
| [UC-010-FE-001: GetCapabilities Falha](./UC-010-FE-001-getcapabilities-falha.md) | ⚠ |
| [UC-010-FE-002: XML Inválido](./UC-010-FE-002-xml-invalido.md) | ⚠ |
| [UC-010-FE-003: Layer Não Encontrado](./UC-010-FE-003-layer-nao-encontrado.md) | ⚠ |
| [UC-010-FE-004: Erro ao Renderizar (Frontend)](./UC-010-FE-004-erro-renderizar.md) | ⚠ |

<!-- CARF-INDEX-END -->
