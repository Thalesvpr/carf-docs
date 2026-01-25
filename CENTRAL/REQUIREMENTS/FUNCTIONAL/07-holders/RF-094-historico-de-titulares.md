---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-094: Historico de Titulares

## Descricao

Sistema deve registrar historico completo de titulares de cada unidade atraves de tabela holder_history capturando data inicio, data termino, tipo de relacionamento, percentual e motivo de alteracao (VENDA, HERANCA, SEPARACAO, DOACAO, REGULARIZACAO, OUTRO). Quando titular e removido ou substituido, registro historico preserva informacao sobre titular anterior. Interface apresenta timeline cronologica de titulares. Valioso para rastreabilidade de direitos e documentacao de processos de regularizacao.

## Criterios de Aceitacao

1. Tabela holder_history com datas e motivo
2. Registro automatico ao remover titular
3. Timeline cronologica de titulares
4. Motivo como enum predefinido
5. Preservacao de percentuais historicos

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-061, RF-060
