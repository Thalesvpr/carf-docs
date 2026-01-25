---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-176: Anexar Documentos ao Processo

## Descricao

Sistema deve permitir upload de documentos comprobatorios vinculados ao processo de legitimacao, incluindo certidoes negativas de debitos, declaracoes de posse, comprovantes de residencia e documentos pessoais dos titulares. Tipologia predefinida classifica cada arquivo conforme natureza juridica ou tecnica, facilitando organizacao e geracao de checklist de completude documental. Sistema compara documentos anexados com lista de documentos obrigatorios para modalidade de regularizacao aplicavel, sinalizando pendencias e calculando percentual de completude. Arquivos armazenados em bucket S3/MinIO com prefixo por tenant_id, validando integridade, formatos aceitos e limites de tamanho conforme politicas de seguranca.

## Criterios de Aceitacao

1. Upload de multiplos tipos de documentos
2. Tipologia predefinida por modalidade REURB
3. Checklist automatico de completude
4. Armazenamento em S3/MinIO por tenant
5. Validacao de formato e tamanho

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-172, RF-102
