---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - REURBCAD
  - GEOAPI
---

# RF-097: Upload de Documentos do Titular

## Descricao

Sistema deve permitir anexacao de documentos pessoais a titulares incluindo RG, CPF, comprovante de residencia, certidoes e declaracoes. Cada documento categorizado por tipo (RG, CPF, COMPROVANTE_RESIDENCIA, CERTIDAO_NASCIMENTO, CERTIDAO_CASAMENTO, DECLARACAO, OUTRO). Interface oferece preview de PDFs e imagens sem download, alem de download individual ou em lote. Documentos vinculados ao titular centralizando gestao documental e permitindo reutilizacao em multiplos vinculos com unidades.

## Criterios de Aceitacao

1. Upload multiplo de documentos
2. Categorizacao por tipo predefinido
3. Preview integrado de PDFs e imagens
4. Download individual e em lote
5. Vinculo ao titular (nao a unidade)

## Rastreabilidade

- Modulos: REURBWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-084, RF-064
