---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-179: Timeline de Processo

## Descricao

Sistema deve apresentar visualizacao cronologica completa do historico de tramitacao do processo de legitimacao atraves de interface de timeline exibindo eventos em ordem temporal reversa. Timeline consolida diferentes tipos de eventos incluindo mudancas de status com justificativas, anexacao de documentos comprobatorios com identificacao de tipo e autor, edicoes de dados cadastrais com registro de campos modificados, geracao de termos oficiais e interacoes como comentarios de analistas ou solicitacoes de complementacao documental. Cada evento apresentado com timestamp preciso, icone diferenciado por tipo, usuario responsavel e descricao textual autoexplicativa. Fundamental para transparencia processual e accountability em processos administrativos publicos.

## Criterios de Aceitacao

1. Exibicao cronologica reversa de eventos
2. Consolidacao de todos os tipos de evento
3. Icones diferenciados por tipo
4. Identificacao de usuario e timestamp
5. Descricao autoexplicativa de cada evento

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-172, RF-173, RF-175, RF-176
