---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-153: Anotacoes (Annotations)

## Descricao

Sistema deve permitir criacao de anotacoes pontuais no mapa combinando localizacao geografica com texto descritivo, permitindo documentacao de observacoes, notas de campo ou marcacoes durante analise e planejamento. Criacao atraves de clique no mapa para definir ponto de localizacao seguido de entrada de texto onde usuario digita observacao em campo apropriado. Anotacoes renderizadas no mapa com icone diferenciado (pin com balao, nota adesiva ou marcador colorido) distinguindo visualmente de outros tipos de features. Listagem de anotacoes em painel lateral apresentando todas do contexto atual ordenadas por data, autor ou localizacao, permitindo navegacao rapida com funcionalidade de zoom para anotacao selecionada. Cada anotacao armazena metadados incluindo autor, timestamp e opcionalmente categoria ou tag.

## Criterios de Aceitacao

1. Criacao via clique no mapa + texto
2. Icone diferenciado para anotacoes
3. Listagem em painel lateral
4. Metadados de autor e timestamp
5. Zoom para anotacao selecionada

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-132, RF-151
