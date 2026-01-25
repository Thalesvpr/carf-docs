---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-064: Anexar Documentos a Unidade

## Descricao

Sistema deve permitir upload de documentos comprobatorios relacionados a unidades habitacionais. Formatos aceitos incluem PDF, JPG, PNG para contratos, comprovantes, certidoes e declaracoes. Cada documento pode ser classificado por tipo configuravel (RG, CPF, COMPROVANTE_RESIDENCIA, CONTRATO, ESCRITURA, DECLARACAO_POSSE, OUTRO). Validacao de tamanho maximo 10MB por arquivo e tipo MIME. Metadados armazenam nome original, tamanho, data de upload, usuario responsavel e hash para verificacao de integridade.

## Criterios de Aceitacao

1. Upload de documentos PDF, JPG, PNG
2. Classificacao por tipo de documento
3. Validacao de tamanho maximo 10MB
4. Validacao de tipo MIME
5. Armazenamento de metadados e hash de integridade

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-049
