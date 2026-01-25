---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-060: Timeline de Unidade

## Descricao

Sistema deve exibir historico completo e cronologico de todas as alteracoes ocorridas em uma unidade habitacional. Timeline apresenta eventos como criacao inicial, edicoes de campos, mudancas de status, vinculacao de titulares e upload de documentos ou fotos. Cada evento registra timestamp preciso, usuario responsavel, tipo de operacao e valores anteriores e novos quando aplicavel. Interface GEOWEB renderiza timeline em ordem cronologica reversa com icones diferenciados por tipo de evento.

## Criterios de Aceitacao

1. Listagem cronologica de todos os eventos da unidade
2. Registro de timestamp e usuario por evento
3. Diferenciacao visual por tipo de evento
4. Valores anterior e novo para campos modificados
5. Ordenacao cronologica reversa com paginacao

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-056
