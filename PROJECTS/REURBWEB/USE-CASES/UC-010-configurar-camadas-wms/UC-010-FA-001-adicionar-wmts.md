---
id: UC-010-FA-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FA-001: Adicionar WMTS

Fluxo alternativo do UC-010 para configurar camada WMTS com tiles pre-renderizados.

## Condicao

No passo 5 do UC-010, ADMIN seleciona tipo WMTS ao inves de WMS.

## Fluxo

1. ADMIN seleciona tipo WMTS
2. Sistema expande formulario com campos adicionais
3. Sistema exibe dropdown TileMatrixSet
4. Sistema exibe dropdown Format (PNG/JPEG)
5. ADMIN clica Testar Conexao
6. Sistema executa GetCapabilities WMTS
7. Sistema pre-popula opcoes conforme servidor
8. ADMIN seleciona TileMatrixSet e formato
9. ADMIN completa configuracao e salva

## Vantagens WMTS

- Tiles pre-gerados com performance superior
- Servidos via CDN sem processamento
- Ideal para ortofotos de alta resolucao
- Cache de navegador otimizado

## Retorno

Camada WMTS configurada com TileMatrixSet e Format especificos.
