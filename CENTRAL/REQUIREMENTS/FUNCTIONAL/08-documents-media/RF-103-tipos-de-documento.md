---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-103: Tipos de Documento

## Descricao

Sistema deve suportar categorizacao de documentos atraves de tipos predefinidos (RG, CPF, COMPROVANTE_RESIDENCIA, CONTRATO, PROCURACAO, ESCRITURA, CERTIDAO, DECLARACAO, OUTRO). Implementacao via enumeracao no campo document_type garantindo valores consistentes. Interface de upload apresenta seletor de tipo obrigatorio com descricoes claras. Filtros por tipo nas interfaces de listagem permitem visualizacao segmentada. Opcao OUTRO acomoda situacoes nao contempladas com campo adicional para especificacao.

## Criterios de Aceitacao

1. Enum com tipos de documento predefinidos
2. Seletor de tipo obrigatorio no upload
3. Filtros por tipo nas listagens
4. Opcao OUTRO com texto livre
5. Descricoes claras de cada tipo

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-102, RF-097
