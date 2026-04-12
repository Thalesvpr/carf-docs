---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-084: Integracao WMS/WMTS

## Descricao

Consumo de servicos WMS (1.1.1, 1.3.0) e WMTS (1.0.0) padrao OGC. Parsing de GetCapabilities para descoberta de layers. Configuracao de multiplas fontes via interface administrativa.

## Metricas

- WMS: versoes 1.1.1 e 1.3.0
- WMTS: versao 1.0.0 com cache de tiles
- GetCapabilities: parsing de XML para descoberta de metadados

## Criterios de Aceitacao

1. Servicos publicos do IBGE e estaduais visualizados corretamente
2. Reprojecao entre CRS diferentes tratada transparentemente
3. Interface administrativa permite adicionar URLs, selecionar layers, configurar opacidade
