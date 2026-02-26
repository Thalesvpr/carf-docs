---
type: leaf
status: approved
updated: 2026-02-21
---

# Ortofoto

Mosaico georreferenciado gerado a partir de imagens capturadas por drone. Representa vista aerea ortogonal da area de interesse com precisao geometrica centimetrica.

Ortofoto e o insumo base para todo o trabalho de georreferenciamento. Operador de Drone captura imagens, processa mosaico, e entrega ao sistema. Backend processa para otimizar tamanho e gera versoes para diferentes usos.

## Caracteristicas Tecnicas

Formato tipico e GeoTIFF ou JPEG2000 com coordenadas embarcadas. Resolucao varia de 2 a 10 centimetros por pixel dependendo da altitude do voo. Arquivos originais podem atingir varios gigabytes.

## Processamento

Backend sempre processa ortofoto recebida:
- Versao original mantida para analise detalhada
- Versao otimizada gerada para visualizacao web (JPEG/WebP)

## Armazenamento

Ortofotos sao armazenadas em bucket (S3/MinIO) segregado por tenant. Estrutura de pastas segue padrao `/{tenant_id}/ortofotos/{ano}/{mes}/` com subpastas para original e otimizada.

## Fluxo no Sistema

1. Operador de Drone entrega ortofoto via portal de upload
2. Backend processa e armazena em bucket do tenant
3. Analista (Plugin QGIS) acessa ortofoto para georreferenciar poligonos
4. Equipe de campo baixa versao offline no pacote temporario

## Referencia

Ver [WORKFLOW-MESTRE](../../WORKFLOW-MESTRE/README.md) para fluxo completo de entrega e uso de ortofotos.
