---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-006: Upload de Arquivos

## Descricao

Sistema deve suportar upload de fotos e documentos ate 20MB por arquivo. Multipart upload permite dividir arquivos grandes, retomar uploads interrompidos e exibir progresso em tempo real.

## Metricas

- Tamanho maximo: 20MB por arquivo
- Velocidade minima: 1MB/s em condicoes normais de rede
- Armazenamento: object storage (S3/MinIO)

## Criterios de Aceitacao

1. Multipart upload obrigatorio para arquivos grandes
2. Barra de progresso funcional com percentual de conclusao
3. Retry automatico em caso de falha de rede ou timeout
