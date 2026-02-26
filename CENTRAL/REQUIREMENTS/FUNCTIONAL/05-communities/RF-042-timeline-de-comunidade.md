---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-042: Timeline de Comunidade

## Descricao

Interface deve exibir historico cronologico de alteracoes da comunidade. Linha do tempo visual apresenta eventos em ordem cronologica reversa com representacao grafica usando icones e marcadores. Eventos registrados incluem criacao inicial, edicoes de dados alfanumericos, modificacoes de geometria, aprovacoes de unidades, desativacao/reativacao e anexacao de documentos. Cada evento exibe usuario responsavel, timestamp preciso e descricao da modificacao.

## Criterios de Aceitacao

1. Linha do tempo em ordem cronologica reversa
2. Eventos de criacao, edicao, geometria e aprovacoes
3. Exibicao de usuario responsavel e timestamp
4. Filtros por tipo de evento e periodo
5. Expansao de detalhes inline

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-035
