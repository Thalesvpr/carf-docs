---
type: workflow
status: approved
updated: 2026-01-25
category: regras
---

# Regras de Processamento de Ortofotos

Regras que garantem o correto processamento e armazenamento de ortofotos.

## Regras

| Regra | Descricao |
|-------|-----------|
| ORTO-01 | Backend SEMPRE reduz o tamanho da ortofoto |
| ORTO-02 | Backend SEMPRE salva ortofoto em bucket (S3/MinIO) |
| ORTO-03 | Ortofoto SEMPRE e associada ao TENANT do analista |
| ORTO-04 | Versao original e versao reduzida DEVEM ser armazenadas |

## Detalhamento

### ORTO-01: Reducao Obrigatoria

O backend sempre processa a ortofoto:
- Gera versao otimizada para web (JPEG/WebP)
- Gera tiles para navegacao eficiente
- Reducao e automatica, nao opcional

### ORTO-02: Armazenamento em Bucket

Ortofotos sao armazenadas em object storage:
- S3 (AWS) ou MinIO (on-premise)
- Estrutura de pastas por TENANT
- URLs presigned para acesso seguro

### ORTO-03: Associacao com TENANT

A ortofoto e automaticamente associada ao TENANT:
- TENANT extraido do token JWT do analista
- Nao e possivel enviar ortofoto para outro TENANT

### ORTO-04: Versoes Multiplas

Duas versoes devem ser mantidas:
- **Original**: Para analise detalhada
- **Reduzida**: Para visualizacao e uso em campo
