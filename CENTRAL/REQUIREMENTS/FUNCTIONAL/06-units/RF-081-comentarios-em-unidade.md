---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-081: Comentarios em Unidade

## Descricao

Sistema deve permitir que usuarios adicionem comentarios e observacoes em unidades criando thread colaborativo de comunicacao assincrona. Cada comentario captura texto livre, timestamp e usuario autor. Thread cronologica ordenada com interface de resposta para comentarios encadeados. Sistema dispara notificacoes automaticas para usuarios envolvidos incluindo criador, gestores e quem previamente comentou. Facilita colaboracao entre analistas e gestores para esclarecimentos, solicitacoes e registro de observacoes de campo.

## Criterios de Aceitacao

1. Adicao de comentarios em unidade
2. Thread cronologica de comentarios
3. Respostas encadeadas
4. Notificacao automatica de envolvidos
5. Timestamp e autor por comentario

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-033
