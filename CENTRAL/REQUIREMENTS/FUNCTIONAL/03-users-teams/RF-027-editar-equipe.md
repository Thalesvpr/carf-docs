---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-027: Editar Equipe

## Descricao

Usuarios com role ADMIN podem editar dados de equipes existentes. Atualizacao inclui modificacao de nome e descricao para refletir mudancas organizacionais ou escopo de responsabilidades. Adicao ou remocao de membros implementada atraves de interface de selecao multipla onde desvinculacao nao afeta historico de trabalho realizado pelo usuario. Log detalhado de alteracoes registra todas modificacoes em equipe incluindo mudancas de membros e atribuicoes de comunidades.

## Criterios de Aceitacao

1. Edicao de nome e descricao da equipe
2. Adicao e remocao de membros via selecao multipla
3. Historico de trabalho preservado apos desvinculacao
4. Log de auditoria registra todas modificacoes
5. Equipe deve manter ao menos um membro ativo

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-026, RF-008
