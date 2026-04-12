---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - REURBCAD
  - GEOAPI
---

# RF-102: Upload de Documentos

## Descricao

Sistema deve permitir upload de documentos em formatos diversos (PDF, DOCX, XLSX, JPG, PNG) via interface drag-and-drop ou selecao de arquivos. Validacao verifica tipo MIME real (nao apenas extensao) bloqueando formatos perigosos. Tamanho maximo 10MB validado em frontend e backend. Sistema armazena metadados completos: nome original, tamanho, tipo MIME, hash SHA-256, timestamp, usuario e entidade vinculada. Conforme WORKFLOW-MESTRE, armazenamento em bucket S3/MinIO segregado por tenant.

## Criterios de Aceitacao

1. Upload via drag-and-drop ou selecao de arquivos
2. Validacao de tipo MIME real
3. Limite de 10MB por arquivo
4. Hash SHA-256 para integridade
5. Metadados completos armazenados

## Rastreabilidade

- Modulos: REURBWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-103, RF-104, RF-116
