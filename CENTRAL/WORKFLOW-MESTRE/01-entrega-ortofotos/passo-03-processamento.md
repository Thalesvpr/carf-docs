---
type: workflow
status: approved
updated: 2026-02-21
part: 1
step: 3
---

# Passo 3: Processamento pelo Backend

Processamento da ortofoto recebida, incluindo reducao e geracao de versoes otimizadas.

## Fluxo

1. Backend recebe ortofoto original
2. Backend extrai metadados (EXIF, coordenadas, data captura)
3. Backend processa e reduz tamanho:
   - Gera versao otimizada para visualizacao web (compressao JPEG/WebP)
   - Mantem versao original para analise detalhada
4. Backend registra metadados no banco de dados

## Versoes Geradas

| Versao | Descricao | Uso |
|--------|-----------|-----|
| Original | Arquivo original sem alteracao | Analise detalhada |
| Otimizada | Compressao JPEG/WebP | Visualizacao web |

## Metadados Extraidos

- Coordenadas geograficas (bounding box)
- Sistema de coordenadas (CRS)
- Data de captura
- Resolucao (pixels por metro)
- Tamanho do arquivo
- Checksum (integridade)

## Resultado

- Ortofoto processada em duas versoes (original e otimizada)
- Metadados extraidos e registrados
- Pronto para armazenamento em bucket

## Proximo Passo

Passo 4: Armazenamento em Bucket
